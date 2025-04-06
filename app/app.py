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
    options=df['Perfil do Cliente'].unique(),
    default=df['Perfil do Cliente'].unique()
)

renda_min, renda_max = st.sidebar.slider(
    "Faixa de Renda Mensal (R$)",
    min_value=int(df['Renda Mensal (R$)'].min()),
    max_value=int(df['Renda Mensal (R$)'].max()),
    value=(int(df['Renda Mensal (R$)'].min()), int(df['Renda Mensal (R$)'].max()))
)

tempo_min, tempo_max = st.sidebar.slider(
    "Tempo como Cliente (meses)",
    min_value=int(df['Tempo como Cliente (meses)'].min()),
    max_value=int(df['Tempo como Cliente (meses)'].max()),
    value=(int(df['Tempo como Cliente (meses)'].min()), int(df['Tempo como Cliente (meses)'].max()))
)

exibir_churn = st.sidebar.checkbox("Mostrar apenas clientes com churn", value=False)

# --- Filtro aplicado
df_filtrado = df[df['Perfil do Cliente'].isin(perfil_selecionado)]
df_filtrado = df_filtrado[(df_filtrado['Renda Mensal (R$)'] >= renda_min) & (df_filtrado['Renda Mensal (R$)'] <= renda_max)]
df_filtrado = df_filtrado[(df_filtrado['Tempo como Cliente (meses)'] >= tempo_min) & (df_filtrado['Tempo como Cliente (meses)'] <= tempo_max)]
if exibir_churn:
    df_filtrado = df_filtrado[df_filtrado['Churn'] == 1]

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
    col2.metric("Churn Médio", f"{df_filtrado['Churn'].mean():.2%}")
    col3.metric("Satisfação Média", f"{df_filtrado['Satisfação'].mean():.2f}")

    st.markdown("""
    A distribuição abaixo mostra como os clientes estão segmentados de acordo com os perfis definidos pelo modelo de clusterização.
    Isso ajuda a entender a proporção de cada grupo dentro da base.
    """)

st.subheader("Distribuição de Clientes por Perfil")

# Contagem de clientes por perfil
contagem_perfil = df_filtrado['Perfil do Cliente'].value_counts().reset_index()
contagem_perfil.columns = ['Perfil do Cliente', 'Quantidade']

# Gráfico de barras com Plotly
fig = px.bar(
    contagem_perfil,
    x='Perfil do Cliente',
    y='Quantidade',
    color='Perfil do Cliente',
    title="Distribuição de Clientes por Perfil",
    text_auto=True
)
fig.update_layout(xaxis_title="", yaxis_title="Quantidade de Clientes")

# Exibição do gráfico no Streamlit
st.plotly_chart(fig, use_container_width=True)

# Explicação
st.markdown(
    "📌 **Interpretação**: Este gráfico mostra a quantidade de clientes em cada perfil identificado via clusterização. "
    "É útil para entender qual segmento representa maior volume de clientes e orientar decisões estratégicas de retenção ou expansão."
)

# --- PERFIS DE CLIENTES ---
elif pagina == "Perfis de Clientes":
    st.title("📈 Análise dos Perfis de Cliente")

    st.subheader("Indicadores Médios por Perfil")
    indicadores = df_filtrado.groupby("Perfil do Cliente")[[
        "Renda Mensal (R$)", "Ticket Médio (R$)", "Compras nos últimos 12 meses",
        "Tempo como Cliente (meses)", "Visitas no Site (més)", "Satisfação", "Churn"
    ]].mean().reset_index()

    st.dataframe(indicadores.style.format({
        "Renda Mensal (R$)": "R$ {:,.2f}",
        "Ticket Médio (R$)": "R$ {:,.2f}",
        "Churn": "{:.2%}"
    }), use_container_width=True)

    st.subheader("Distribuição de Métricas de Negócio")
    st.markdown("""
    Este gráfico permite comparar como diferentes perfis de clientes se comportam em relação à métrica selecionada.
    """)
    metrica = st.selectbox("Escolha a métrica", [
        "Renda Mensal (R$)", "Ticket Médio (R$)", "Compras nos últimos 12 meses",
        "Tempo como Cliente (meses)", "Visitas no Site (més)", "Satisfação"
    ])

    fig_box = px.violin(df_filtrado, x="Perfil do Cliente", y=metrica, color="Perfil do Cliente", box=True, points="all")
    st.plotly_chart(fig_box, use_container_width=True)

# --- ANÁLISES AVANÇADAS ---
elif pagina == "Análises Avançadas":
    st.title("🔬 Análises Avançadas")

    st.subheader("Visualização de Clusters (PCA)")
    st.markdown("""
    O gráfico abaixo é uma redução das variáveis para duas dimensões (PCA), permitindo visualizar a distribuição dos perfis em um espaço de similaridade.
    """)
    fig_pca = px.scatter(df_filtrado, x="PCA 1", y="PCA 2", color="Perfil do Cliente",
                         hover_data=['Churn', 'Satisfação'])
    st.plotly_chart(fig_pca, use_container_width=True)

    st.subheader("Correlação entre Variáveis")
    st.markdown("""
    A matriz de correlação mostra como as variáveis numéricas estão relacionadas. Valores próximos de 1 indicam correlação positiva forte; próximos de -1, negativa.
    """)
    corr_df = df_filtrado.select_dtypes(include='number').drop(columns=['PCA 1', 'PCA 2'])
    corr_matrix = corr_df.corr().round(2)

    fig_corr = go.Figure(data=go.Heatmap(
        z=corr_matrix.values,
        x=corr_matrix.columns,
        y=corr_matrix.index,
        colorscale='RdBu', zmin=-1, zmax=1,
        colorbar=dict(title="Correlação")
    ))
    st.plotly_chart(fig_corr, use_container_width=True)