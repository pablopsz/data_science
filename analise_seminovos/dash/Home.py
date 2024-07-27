import pandas as pd
import streamlit as st
from utils.graph_lib import GraphLib

st.set_page_config(page_title="Análise de Seminovos", layout="centered", page_icon=":car:")

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

    st.title("Análise de Seminovos")

    df = load_data("E:\\Workspace\\analise_seminovos\\df_main\\df_consol.csv")

    if df.empty:
        st.error("Erro ao carregar dados. Por favor, verifique o arquivo e tente novamente.")
        return

    min_date, max_date = df['data_atual'].min(), df['data_atual'].max()

    st.sidebar.header("Filtros")

    col1, col2 = st.columns(2)
    with col1:
        first_date = st.date_input("Data Inicial", min_date, min_date, max_date)
    with col2:
        last_date = st.date_input("Data Final", max_date, min_date, max_date)

    all_brands = sorted(df[(df['data_atual'] >= pd.to_datetime(first_date)) & (df['data_atual'] <= pd.to_datetime(last_date))]['marca'].unique().tolist())
    selected_brands = st.sidebar.multiselect('Selecione as marcas', all_brands)
    select_all_brands = st.sidebar.checkbox('Selecionar todas as marcas', value=False)

    if select_all_brands:
        selected_brands = all_brands

    all_models = sorted(df[df['marca'].isin(selected_brands)]['modelo'].unique().tolist())
    selected_models = st.sidebar.multiselect('Selecione os modelos', all_models)
    select_all_models = st.sidebar.checkbox('Selecionar todos os modelos', value=False)

    if select_all_models:
        selected_models = all_models

    df_filtered = df.query("marca in @selected_brands and modelo in @selected_models and data_atual >= @first_date and data_atual <= @last_date")

    if df_filtered.empty:
        st.warning("Nenhum dado encontrado para os filtros selecionados.")
        return

    col1, col2, col3 = st.columns(3)
    with col1:

        st.metric("Total de Veículos Analisados", (df_filtered["id"].nunique()))
    with col2:

        st.metric("Média de Preço", f'R$ {round(df_filtered['preco'].mean(),2)}')
    with col3:
        st.metric("Média de KM", round(df_filtered['quilometragem'].mean(),2))

    df_filtered_gp = df_filtered.groupby(['data_atual', 'modelo']).agg({
    'preco': 'mean',
    'quilometragem': 'mean'}).reset_index()

    tab1, tab2, tab3 = st.tabs(["Preço", "Quilometragem", "Dados Filtrados"])

    with tab1:
        fig_price = generate_line_chart(df_filtered_gp, 'data_atual', 'preco', 'Preço de Veículos', 'modelo')
        st.plotly_chart(fig_price)

    with tab2:
        fig_km = generate_line_chart(df_filtered_gp, 'data_atual', 'quilometragem', 'Quilometragem de Veículos', 'modelo')
        st.plotly_chart(fig_km)

    with tab3:
        st.write(df_filtered_gp)

setup_dash()
