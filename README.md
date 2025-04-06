# 📊 Segmentação de Clientes com K-Means

Este projeto realiza uma análise de dados de clientes fictícios para segmentação usando machine learning (K-Means) e apresenta os resultados em um dashboard interativo com Streamlit.

## 🔍 Objetivo

Identificar perfis de clientes e gerar insights para retenção e crescimento das vendas com base em comportamento de compra, engajamento digital e satisfação.

## 🚀 Funcionalidades

- Geração de base de dados sintética
- Análise exploratória dos dados
- Clusterização com K-Means
- Nomeação e interpretação de perfis
- Dashboard com métricas e visualizações

## 🖥️ Tecnologias

- Python
- Pandas, Scikit-learn, Plotly
- Streamlit
- GitHub Codespaces

## 📊 Dashboard

O dashboard permite explorar:
- Distribuição de clientes por perfil
- Indicadores por perfil (churn, satisfação, ticket médio etc.)
- Visualização dos clusters via PCA

## 📁 Organização

```
data/                 # Dados utilizados
notebooks/            # Análises e EDA
src/                  # Scripts auxiliares
app/app.py            # Código do dashboard
```

## ▶️ Executar localmente

```bash
pip install -r requirements.txt
streamlit run app/app.py
```

## ☁️ Deploy

O app pode ser publicado gratuitamente no [Streamlit Cloud](https://streamlit.io/cloud).

## ✍️ Autor

Projeto desenvolvido por Alexandre Kulpel como parte de portfólio de ciência de dados.

