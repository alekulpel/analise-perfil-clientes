import streamlit as st
import pandas as pd
import plotly.express as px

# --- Configuração inicial
st.set_page_config(page_title="Dashboard de Clientes", layout="wide")

# --- Carregar dados
@st.cache_data
def carregar_dados():
    return pd.read_csv('data/processed/clientes_com_perfil.csv')

df = carregar_dados()

# --- Título
st.title("📊 Dashboard de Segmentação de Clientes")

# --- Filtros
st.sidebar.header("Filtros")
perfil_selecionado = st.sidebar.multiselect(
    "Perfis de Cliente",
    options=df['perfil_cliente'].unique(),
    default=df['perfil_cliente'].unique()
)

df_filtrado = df[df['perfil_cliente'].isin(perfil_selecionado)]

# --- Métricas principais
st.subheader("Visão Geral")
col1, col2, col3 = st.columns(3)
col1.metric("Total de Clientes", len(df_filtrado))
col2.metric("Churn Médio", f"{df_filtrado['churn'].mean():.2%}")
col3.metric("Satisfação Média", f"{df_filtrado['satisfacao'].mean():.2f}")

# --- Distribuição por perfil
st.subheader("Distribuição de Clientes por Perfil")
fig = px.histogram(df_filtrado, x="perfil_cliente", color="perfil_cliente", barmode="group")
st.plotly_chart(fig, use_container_width=True)

# --- Métricas por perfil
st.subheader("Indicadores Médios por Perfil")
indicadores = df_filtrado.groupby("perfil_cliente")[[
    "renda_mensal", "ticket_medio", "qtd_compras_ultimos_12m",
    "tempo_como_cliente", "visitas_site_mes", "satisfacao", "churn"
]].mean().reset_index()

st.dataframe(indicadores.round(2))

# --- Gráficos comparativos
st.subheader("Distribuição de Métricas por Perfil")

metrica = st.selectbox("Escolha a métrica", [
    "renda_mensal", "ticket_medio", "qtd_compras_ultimos_12m",
    "tempo_como_cliente", "visitas_site_mes", "satisfacao"
])

fig_box = px.box(df_filtrado, x="perfil_cliente", y=metrica, color="perfil_cliente", points="all")
st.plotly_chart(fig_box, use_container_width=True)

# --- Visualização PCA
st.subheader("Visualização de Clusters (PCA)")
fig_pca = px.scatter(df_filtrado, x="pca1", y="pca2", color="perfil_cliente", hover_data=['churn', 'satisfacao'])
st.plotly_chart(fig_pca, use_container_width=True)