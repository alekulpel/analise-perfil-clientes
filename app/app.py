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

# --- Sidebar: Navegação e filtros
st.sidebar.title("🔍 Navegação")
pagina = st.sidebar.selectbox("Escolha a página", [
    "Visão Geral", "Perfis de Clientes", "Análises Avançadas"])

st.sidebar.header("Filtros")
perfil_selecionado = st.sidebar.multiselect(
    "Perfis de Cliente",
    options=df['perfil_cliente'].unique(),
    default=df['perfil_cliente'].unique()
)

renda_min, renda_max = st.sidebar.slider(
    "Faixa de Renda Mensal (R$)",
    min_value=int(df['renda_mensal'].min()),
    max_value=int(df['renda_mensal'].max()),
    value=(int(df['renda_mensal'].min()), int(df['renda_mensal'].max()))
)

tempo_min, tempo_max = st.sidebar.slider(
    "Tempo como Cliente (meses)",
    min_value=int(df['tempo_como_cliente'].min()),
    max_value=int(df['tempo_como_cliente'].max()),
    value=(int(df['tempo_como_cliente'].min()), int(df['tempo_como_cliente'].max()))
)

exibir_churn = st.sidebar.checkbox("Mostrar apenas clientes com churn", value=False)

# --- Filtro aplicado
df_filtrado = df[df['perfil_cliente'].isin(perfil_selecionado)]
df_filtrado = df_filtrado[(df_filtrado['renda_mensal'] >= renda_min) & (df_filtrado['renda_mensal'] <= renda_max)]
df_filtrado = df_filtrado[(df_filtrado['tempo_como_cliente'] >= tempo_min) & (df_filtrado['tempo_como_cliente'] <= tempo_max)]
if exibir_churn:
    df_filtrado = df_filtrado[df_filtrado['churn'] == 1]

# --- Botão para exportar CSV
csv = df_filtrado.to_csv(index=False).encode('utf-8')
st.sidebar.download_button(
    label="📂 Baixar dados filtrados",
    data=csv,
    file_name='clientes_filtrados.csv',
    mime='text/csv'
)

# --- VISÃO GERAL ---
if pagina == "Visão Geral":
    st.title("📊 Dashboard de Segmentação de Clientes")

    st.subheader("Visão Geral")
    col1, col2, col3 = st.columns(3)
    col1.metric("Total de Clientes", len(df_filtrado))
    col2.metric("Churn Médio", f"{df_filtrado['churn'].mean():.2%}")
    col3.metric("Satisfação Média", f"{df_filtrado['satisfacao'].mean():.2f}")

    st.subheader("Distribuição de Clientes por Perfil")
    fig = px.histogram(df_filtrado, x="perfil_cliente", color="perfil_cliente", barmode="group")
    st.plotly_chart(fig, use_container_width=True)

# --- PERFIS DE CLIENTES ---
elif pagina == "Perfis de Clientes":
    st.title("📈 Análise dos Perfis de Cliente")

    st.subheader("Indicadores Médios por Perfil")
    indicadores = df_filtrado.groupby("perfil_cliente")[[
        "renda_mensal", "ticket_medio", "qtd_compras_ultimos_12m",
        "tempo_como_cliente", "visitas_site_mes", "satisfacao", "churn"
    ]].mean().reset_index()

    st.dataframe(indicadores.round(2), use_container_width=True)

    st.subheader("Distribuição de Métricas por Perfil")
    metrica = st.selectbox("Escolha a métrica", [
        "renda_mensal", "ticket_medio", "qtd_compras_ultimos_12m",
        "tempo_como_cliente", "visitas_site_mes", "satisfacao"
    ])

    fig_box = px.box(df_filtrado, x="perfil_cliente", y=metrica, color="perfil_cliente", points="all")
    st.plotly_chart(fig_box, use_container_width=True)

# --- ANÁLISES AVANÇADAS ---
elif pagina == "Análises Avançadas":
    st.title("🔬 Análises Avançadas")

    st.subheader("Visualização de Clusters (PCA)")
    fig_pca = px.scatter(df_filtrado, x="pca1", y="pca2", color="perfil_cliente", hover_data=['churn', 'satisfacao'])
    st.plotly_chart(fig_pca, use_container_width=True)

    st.subheader("Correlação entre variáveis")
    correlacao = df_filtrado.drop(columns=['pca1', 'pca2']).corr()
    st.dataframe(correlacao.round(2), use_container_width=True)
