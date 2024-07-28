import streamlit as st
import pandas as pd
from utils.graph_lib import GraphLib

@st.cache_data
def load_data(filepath):
    try:
        df = pd.read_csv(filepath, sep=",", dtype={'data_atual': str, 'ano_fabricacao': str}) 
        df['data_atual'] = pd.to_datetime(df['data_atual'], format='%d%m%Y', errors='coerce')
        df = df.dropna(subset=['data_atual', 'ano_fabricacao']) 
        return df
    except Exception as e:
        st.error(f"Erro ao carregar dados: {e}")
        return pd.DataFrame()
    
@st.cache_data
def generate_line_chart(df, x_col, y_col, title, color):
    fig = GraphLib.line_chart(df, x_col, y_col, title, color)
    return fig

def setup_dash():
    st.title('Estoque')

    df = load_data("E:\\Workspace\\analise_seminovos\\df_main\\df_consol.csv")

    min_data, max_data = df['data_atual'].min(), df['data_atual'].max()

    st.sidebar.header('Filtros')

    col1, col2 = st.columns(2)

    with col1:
        first_date = st.date_input('Data Inicial', min_data, min_data, max_data)
    
    with col2:
        second_date = st.date_input('Data Final', max_data, min_data, max_data)

    all_brands = sorted(df[(df['data_atual'] >= pd.to_datetime(first_date)) & (df['data_atual'] <= pd.to_datetime(second_date))]['marca'].unique().tolist())
    selected_brands = st.sidebar.multiselect('Selecione as marcas', all_brands)
    select_all_brands = st.sidebar.checkbox('Selecionar todas as marcas', value=False)

    if select_all_brands:
        selected_brands = all_brands

    all_models = sorted(df[df['marca'].isin(selected_brands)]['modelo'].unique().tolist())
    selected_models = st.sidebar.multiselect('Selecione os modelos', all_models)
    select_all_models = st.sidebar.checkbox('Selecionar todos os modelos', value=False)

    if select_all_models:
        selected_models = all_models

    df_filtered = df.query('marca in @selected_brands and modelo in @selected_models and data_atual >= @first_date and data_atual <= @second_date')

    if df_filtered.empty:
        st.warning('Nenhum dado encontrado para os filtros selecionados.')
        return

    df_grouped_stock_brand = df_filtered.groupby(['marca', 'data_atual']).size().reset_index(name='count')

    df_grouped_stock_model = df_filtered.groupby(['modelo', 'data_atual']).size().reset_index(name='count')

    tab1, tab2 = st.tabs(['Estoque por Marca', 'Estoque por Modelo'])

    with tab1:
        fig = generate_line_chart(df_grouped_stock_brand, 'data_atual', 'count', 'Estoque por Marca', 'marca')
        st.plotly_chart(fig)

    with tab2:
        fig = generate_line_chart(df_grouped_stock_model, 'data_atual', 'count', 'Estoque por Modelo', 'modelo')
        st.plotly_chart(fig)

setup_dash()