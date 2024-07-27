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
    df = load_data("E:\\Workspace\\analise_seminovos\\df_main\\df_consol.csv")
    st.title('Tempo de Estoque')
    df = df.sort_values(by=['id', 'data_atual'])
    df['dias_em_estoque'] = df.groupby('id').cumcount() + 1

    st.sidebar.header('Filtros')

    min_data, max_data = df['data_atual'].min(), df['data_atual'].max()

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

    all_models = sorted(df[(df['data_atual'] >= pd.to_datetime(first_date)) & (df['data_atual'] <= pd.to_datetime(second_date)) & (df['marca'].isin(selected_brands))]['modelo'].unique().tolist())
    selected_models = st.sidebar.multiselect('Selecione os modelos', all_models)
    select_all_models = st.sidebar.checkbox('Selecionar todos os modelos', value=False)

    if select_all_models:
        selected_models = all_models

    df_filtered = df.query('marca in @selected_brands and modelo in @selected_models and data_atual >= @first_date and data_atual <= @second_date')

    if df_filtered.empty:
        st.warning('Nenhum dado encontrado para os filtros selecionados.')
        return

    df_grouped_brand = df_filtered.groupby(["marca", "data_atual"]).agg({"dias_em_estoque": "mean"}).reset_index()

    df_grouped_model = df_filtered.groupby(["modelo", "data_atual"]).agg({"dias_em_estoque": "mean"}).reset_index()
    
    tabs = st.tabs(['Tempo de Estoque por Marca', 'Tempo de Estoque por Modelo'])

    with tabs[0]:
        fig = generate_line_chart(df_grouped_brand, 'data_atual', 'dias_em_estoque', 'Tempo de Estoque por Marca', 'marca')
        st.plotly_chart(fig)

    with tabs[1]:
        fig = generate_line_chart(df_grouped_model, 'data_atual', 'dias_em_estoque', 'Tempo de Estoque por Modelo', 'modelo')
        st.plotly_chart(fig)

setup_dash()
