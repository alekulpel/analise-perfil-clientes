import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# --- Configuração inicial
st.set_page_config(page_title="Dashboard de Clientes", layout="wide")

# --- Carregar dados
@st.cache_data
def carregar_dados():
    return pd.read_csv('data/processed/clientes_com_perfil.csv')

df = carregar_dados()

# Renomear colunas para nomes mais amigáveis
colunas_renomeadas = {
    "renda_mensal": "Renda Mensal (R$)",
    "ticket_medio": "Ticket Médio (R$)",
    "qtd_compras_ultimos_12m": "Compras nos últimos 12 meses",
    "tempo_como_cliente": "Tempo como Cliente (meses)",
    "visitas_site_mes": "Visitas no Site (més)",
    "satisfacao": "Satisfação",
    "churn": "Churn",
    "perfil_cliente": "Perfil do Cliente",
    "pca1": "PCA 1",
    "pca2": "PCA 2"
}
df = df.rename(columns=colunas_renomeadas)

# --- Sidebar: Navegação e filtros
st.sidebar.title("🔍 Navegação")
pagina = st.sidebar.selectbox("Escolha a página", [
    "Visão Geral", "Perfis de Clientes", "Análises Avançadas"])

st.sidebar.header("Filtros")
perfil_selecionado = st.sidebar.multiselect(
    "Perfis de Cliente",
    options
