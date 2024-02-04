import json
import pandas as pd
import openpyxl
import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
from PIL import Image
import matplotlib.pyplot as plt
import numpy as np
import matplotlib.patches as patches
from io import BytesIO

st.set_page_config(page_title="TRAPAS", page_icon=":hammer_and_pick:",layout="wide")

#Logo UFPR 
file_path = "Dashboard/Imagens/UFPR.png"
ufpr_logo = Image.open(file_path)
st.image(ufpr_logo)

# Custom inline style to apply position: sticky
custom_style = "position: -webkit-sticky; position: sticky; top: 0; left: 0;"


st.text("")

st.title('Projeto TRAPAS - Banco de Dados de Sergipe')

df = pd.read_excel(
    io='Dashboard/Dados/DadosBrutos.xlsx',
    engine= 'openpyxl',
    sheet_name='Planilha1',
    skiprows= 0,
    usecols='A:Z',
    nrows=23,
)


#Sidebar

st.sidebar.header("Por favor selecione os dados:")
col = "Polígono"
Polígono = sorted(df['Polígono'].unique())
default_option_1 = "Selecione"
filter_1 = st.sidebar.selectbox(f"Selecione o {col}", [default_option_1] + Polígono)
mask_1 = df['Polígono'].isin(Polígono)
filtered_gr= df[mask_1]

# Create a list of tuples containing both 'PETRO' and 'ANP' options
combined_options = [(petro, anp) for petro, anp in zip(
    sorted(df[df['Polígono'] == filter_1]['PETRO'].unique()),
    sorted(df[df['Polígono'] == filter_1]['ANP'].unique())
)]

# Add a default option
default_option_2 = "Selecione"
filter_2 = st.sidebar.selectbox(f"Selecione o Poço", [default_option_2] + combined_options)


# Determine whether the selected option is from PETRO or ANP
if filter_2 != default_option_2:
    selected_poco = filter_2[0] if filter_2[0] else filter_2[1]
else:
    selected_poco = None

# Filter the dataframe based on selected values
mask_2 = (df['PETRO'] == selected_poco) | (df['ANP'] == selected_poco)
filtered_data = df[mask_1 & mask_2]

#BOTÃO
class SessionState:
    def __init__(self, **kwargs):
        self._state = kwargs

    def get(self, attr, default=None):
        return self._state.get(attr, default)

    def set(self, attr, value):
        self._state[attr] = value

# ... (the rest of your code remains unchanged)

# Create a session state object
session_state = SessionState(show_image_mapa=False, show_image_divisao=False)

# Display the image if the button was clicked for Mapa
if st.sidebar.button('Mapa Divisão Espessura X Número de Camadas de Arenito'):
    # Store the state in the session for the second image
    session_state.set('show_image_divisao', True)
    session_state.set('show_image_mapa', False)

# Display the second image (Divisao)
if session_state.get('show_image_divisao'):
    image_divisao = Image.open(r'Dashboard/Imagens/Divisão.png')
    st.image(image_divisao)

    # Add a button to close the image
    if st.button('Close Divisao Image'):
        session_state.set('show_image_divisao', False)

# Display the image if the button was clicked for Mapa
if st.sidebar.button('Mapa Isópacas de Arenito'):
    # Store the state in the session for the first image
    session_state.set('show_image_mapa', True)
    session_state.set('show_image_divisao', False)

# Display the first image (Mapa)
if session_state.get('show_image_mapa'):
    image_mapa = Image.open(r'Dashboard/Imagens/Mapa de Isópacas.png')
    st.image(image_mapa)

    # Add a button to close the image
    if st.button('Close Mapa Image'):
        session_state.set('show_image_mapa', False)

# Create a list of tuples containing both 'PETRO' and 'ANP' options
#combined_options = [(petro, anp) for petro, anp in zip(sorted(df[df['Polígono'] == filter_1]['PETRO'].unique()), sorted(df[df['Polígono'] == filter_1]['ANP'].unique()))]

# Add a default option
#default_option_2 = "Selecione"
#filter_2 = st.sidebar.selectbox(f"Selecione o Poço", [default_option_2] + combined_options)

# Determine whether the selected option is from PETRO or ANP
#if filter_2 != default_option_2:
    #selected_poco = filter_2[0] if filter_2[0] else filter_2[1]
#else:
    #selected_poco = None

# Filter the dataframe based on selected values
#mask_2 = (df['PETRO'] == selected_poco) | (df['ANP'] == selected_poco)
#filtered_data = df[mask_1 & mask_2]

with st.expander("Data Preview"):
    final_mask = mask_1 & mask_2
    filtered_df = df[final_mask].copy()
    st.dataframe(filtered_df, hide_index=True)


#Colunas
left_column, right_column = st.columns(2)

with left_column:
        st.subheader("Dados gerais do Poço Selecionado:")
        st.text("")
        st.text("")
        filtered_data = df[mask_1 & mask_2] 
        if not filtered_data.empty:
            col1, col2 = st.columns([1, 2])
            with col1:
                st.write("Longitude:") 
                st.write("Latitude:") 
                st.text("")
                st.text("")
                st.write("Cota Batimétrica:")
                st.write("Mesa Rotativa:")
                st.write("Profundidade Final do Poço:")
                st.text("")
                st.write("Topo da Formação Calumbi:")
                st.text("")
                st.write("Base da Formação Calumbi:")
                st.text("")
                st.write("Formação Final:")

            with col2:
             # Use st.write to display the text information
                st.write(filtered_data['Longitude (X)'].to_string(index=False))
                st.write(filtered_data['Latitude (Y)'].to_string(index=False))
                st.text("")
                st.text("")
                st.write(filtered_data['Cota Batimétrica (m)'].to_string(index=False))
                st.write(filtered_data['Mesa Rotativa (m)'].to_string(index=False))
                st.write(filtered_data['Profundidade Final (m)'].to_string(index=False))
                st.text("")
                st.write(filtered_data['Topo Fm. Calumbi (m)'].to_string(index=False))
                st.text("")
                st.write(filtered_data['Base Fm. Calumbi (m) - Marcada no perfil'].to_string(index=False))
                st.text("")
                st.write(filtered_data['Formação Final Marcada'].to_string(index=False))         
            st.text("")
            st.text("")
            # First plot
            stats_by_polygon = filtered_gr.groupby('Polígono').agg({
                'Espessura de Arenito Fm. Calumbi': 'mean',
                'Número de Ocorrências de Arenito Fm. Calumbi': 'sum'
            }).reset_index()

            fig1 = go.Figure()

            fig1.add_trace(go.Bar(
             x=stats_by_polygon['Polígono'],
            y=stats_by_polygon['Espessura de Arenito Fm. Calumbi'],
            name='Média Espessura (m)',
            marker_color='orange'
         ))

            fig1.add_trace(go.Bar(
            x=stats_by_polygon['Polígono'],
            y=stats_by_polygon['Número de Ocorrências de Arenito Fm. Calumbi'],
            name='Total Ocorrências',
            marker_color='green'
        ))

            fig1.update_layout(barmode='group')

            fig1.update_layout(
                legend=dict(orientation='h', y=-0.2, x=0.5),
                legend_title='Legenda:',
                xaxis=dict(
                title='Polígono',
                ),
                yaxis=dict(
                    title='Espessura/Ocorrência (m)',
                ),
            )

            # Second plot
            stats_by_petro = filtered_data.groupby('PETRO').agg({
                'Espessura de Arenito Fm. Calumbi': 'mean',
                'Número de Ocorrências de Arenito Fm. Calumbi': 'sum'
            }).reset_index()

            fig2 = px.bar(
                stats_by_petro,
                x='PETRO',
                y=['Espessura de Arenito Fm. Calumbi', 'Número de Ocorrências de Arenito Fm. Calumbi'],
                labels={'Espessura de Arenito Fm. Calumbi': 'Média Espessura (m)', 'Número de Ocorrências de Arenito Fm. Calumbi': 'Total Ocorrências'},
                barmode='group',
                color_discrete_sequence=['orange', 'green'],
            )

            fig2.update_layout(
                legend=dict(orientation='h', y=-0.2, x=0.5),
                legend_title='Legenda:',
                xaxis=dict(
                    title='Poço',
                ),
                yaxis=dict(
                    title='Espessura/Ocorrência (m)',
                ),
            )

            # Show the plots
            st.plotly_chart(fig2)
            st.plotly_chart(fig1)

        else:
            st.write("Nenhum dado corresponde aos filtros selecionados.")

# Coluna da Direita
with right_column:
    file_path = "Dashboard/Imagens/Imagem_Poligono.png"
    poligon = Image.open(file_path)
    resized_poligon = poligon.resize((500, 500))
    st.image(resized_poligon)

    st.subheader("Outras informações e dados do Poço Selecionado:")
    st.text("")
    st.text("")
    filtered_data = df[mask_1 & mask_2] 

    if not filtered_data.empty:
        col1, col2 = st.columns([1, 2])

        with col1:
            st.text("Perfil Composto:")
            st.text("") 
            st.text("Testemunhos:")
            st.text("")
            st.text("Amostras Laterais:")
            st.text("") 
            st.text("Lâminas:")

        with col2:
            # Displaying hyperlinks with conditional checking
            perfil_composto_link = filtered_data['Perfil Composto'].iloc[0]
            if perfil_composto_link != 'X':
                st.markdown(f"[Perfil Composto]({perfil_composto_link})")
            else:
                st.text("Perfil Composto: No link available")

            st.text("")

            testemunhos_link = filtered_data['Testemunhos'].iloc[0]
            if testemunhos_link != 'X':
                st.markdown(f"[Testemunhos]({testemunhos_link})")
            else:
                st.text("Testemunhos: No link available")

            st.text("")

            amostras_laterais_link = filtered_data['Amostras Laterais'].iloc[0]
            if amostras_laterais_link != 'X':
                st.markdown(f"[Amostras Laterais]({amostras_laterais_link})")
            else:
                st.text("Amostras Laterais: No link available")

            st.text("")

            laminas_link = filtered_data['Lâminas'].iloc[0]
            if laminas_link != 'X':
                st.markdown(f"[Lâminas]({laminas_link})")
            else:
                st.text("Lâminas: No link available")
    else:
        st.write("Nenhum dado corresponde aos filtros selecionados.")

st.text("") 
st.text("") 
st.text("")

#Logo Petrobras 
file_path = "Dashboard/Imagens/Petro.jpg"
petrobr_logo = Image.open(file_path)
resized_petrobr_logo = petrobr_logo.resize((180, 50))

#Logo Labap
file_path = "Dashboard/Imagens/Arquivos_Finais_Logo_LABAP_COR_H(4).png"
labap_logo = Image.open(file_path)
resized_labap_logo = labap_logo.resize((180, 50))

#Logo Geopost        
file_path = "Dashboard/Imagens/geopost_logo.png"
geopost_logo = Image.open(file_path)
resized_geopost_logo = geopost_logo.resize((180, 60))


col1, col2, col3, col4 = st.columns(4)

with col1:
    st.image(resized_petrobr_logo)

with col2:
    st.image(resized_labap_logo)
with col3:
    st.image(resized_geopost_logo)
with col4:
     st.text("")     
     st.markdown('<div style="font-size: 18px;">Construído por: Lorena Alfaro</div>', unsafe_allow_html=True)
