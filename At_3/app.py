import streamlit as st
import pandas as pd
import numpy as np
import plotly.figure_factory as ff
import plotly.express as px

# =========================
# CONFIGURAÇÃO
# =========================
st.set_page_config(
    page_title="Dashboard de Funcionários",
    layout="wide"
)

st.title("📊 Dashboard de Análise de Funcionários")

# =========================
# GERAR DADOS (OU CARREGAR CSV)
# =========================
@st.cache_data
def carregar_dados():
    dados = {
        "nome": ["Ana", "Bruno", "Carlos", "Daniela", "Eduardo"],
        "idade": [23, 35, 29, np.nan, 40],
        "cidade": ["SP", "RJ", "SP", "MG", "RJ"],
        "salario": [3000, 5000, 4000, 3500, np.nan],
        "data_contratacao": pd.to_datetime([
            "2020-01-10", "2019-03-15", "2021-07-22", "2018-11-30", "2022-05-10"
        ])
    }

    df = pd.DataFrame(dados)

    # Limpeza
    df["idade"] = df["idade"].fillna(df["idade"].mean())
    df["salario"] = df["salario"].fillna(df["salario"].median())

    # Feature engineering
    df["salario_anual"] = df["salario"] * 12
    df["ano_contratacao"] = df["data_contratacao"].dt.year

    df["categoria_salario"] = df["salario"].apply(
        lambda x: "Alto" if x > 4500 else "Médio" if x > 3000 else "Baixo"
    )

    return df

df = carregar_dados()


# =========================
# UPLOAD DE ARQUIVO 
# =========================
st.sidebar.subheader("📂 Upload de CSV")
uploaded_file = st.sidebar.file_uploader("Envie um CSV", type=["csv"])

if uploaded_file:
    df_base = pd.read_csv(uploaded_file)
    df_base["data_contratacao"] = pd.to_datetime(df_base["data_contratacao"])
    df_base["idade"] = df_base["idade"].fillna(df_base["idade"].mean())
    df_base["salario"] = df_base["salario"].fillna(df_base["salario"].median())
    df_base["salario_anual"] = df_base["salario"] * 12
    df_base["ano_contratacao"] = df_base["data_contratacao"].dt.year
    df_base["categoria_salario"] = df_base["salario"].apply(
        lambda x: "Alto" if x > 4500 else "Médio" if x > 3000 else "Baixo"
    )
else:
    df_base = df

# =========================
# SIDEBAR (FILTROS)
# =========================
st.sidebar.header("🔎 Filtros")

cidades = st.sidebar.multiselect(
    "Selecione a cidade",
    options=df_base["cidade"].unique(),
    default=df_base["cidade"].unique()
)

faixa_salario = st.sidebar.slider(
    "Faixa salarial",
    float(df_base["salario"].min()),
    float(df_base["salario"].max()),
    (float(df_base["salario"].min()), float(df_base["salario"].max()))
)

categoria = st.sidebar.selectbox(
    "Selencione uma categoria",
    ("Alto", "Médio", "Baixo"),
    index = None
)

df_filtrado = df_base[
    (df_base["cidade"].isin(cidades)) &
    (df_base["salario"] >= faixa_salario[0]) &
    (df_base["salario"] <= faixa_salario[1]) &
    (df_base["categoria_salario"] == categoria)
]


# =========================
# KPIs
# =========================
col1, col2, col3 = st.columns(3)

col1.metric("💰 Salário Médio", f"R$ {df_filtrado['salario'].mean():.2f}")
col2.metric("👥 Total Funcionários", df_filtrado.shape[0])
col3.metric("📈 Salário Máximo", f"R$ {df_filtrado['salario'].max():.2f}")

# =========================
# TABELA
# =========================
st.subheader("📋 Dados")
st.dataframe(df_filtrado, use_container_width=True)

# =========================
# GRÁFICOS
# =========================
st.subheader("📊 Análises")
col1, col2 = st.columns(2)

hist_data = [df_filtrado[df_filtrado["cidade"] == c]["salario"].values
             for c in df_filtrado["cidade"].unique()]
group_labels = list(df_filtrado["cidade"].unique())

with col1:
    if len(df_filtrado) > 0:
        fig_dist = px.histogram(
            df_filtrado,
            x="salario",
            color="cidade",
            barmode="overlay",
            nbins=20,
            title="Distribuição Salarial por Cidade",
            labels={"salario": "Salário", "cidade": "Cidade"},
            color_discrete_sequence=px.colors.qualitative.Set2,
            opacity=0.75
        )

        fig_dist.update_traces(
            hovertemplate="<b>Cidade: %{legendgroup}</b><br>Salário: R$ %{x:.2f}<br>Contagem: %{y}<extra></extra>"
        )

        fig_dist.update_layout(
            xaxis_title="Salário (R$)",
            yaxis_title="Nº de Funcionários",
            legend_title="Cidade"
        )

        st.plotly_chart(fig_dist, use_container_width=True)

with col2:
    contagem_categoria = df_filtrado["categoria_salario"].value_counts().reset_index()
    contagem_categoria.columns = ["Categoria", "Quantidade"]

    fig_bar = px.bar(
        contagem_categoria,
        x="Categoria",
        y="Quantidade",
        color="Categoria",
        color_discrete_map={
            "Alto": "#2ecc71",
            "Médio": "#f39c12",
            "Baixo": "#e74c3c"
        },
        title="Distribuição por Categoria Salarial",
        hover_data={"Categoria": True, "Quantidade": True},
        labels={"Quantidade": "Nº de Funcionários"}
    )

    fig_bar.update_traces(
        hovertemplate="<b>%{x}</b><br>Funcionários: %{y}<extra></extra>"
    )

    fig_bar.update_layout(
        showlegend=False,
        xaxis_title="Categoria",
        yaxis_title="Nº de Funcionários"
    )

    st.plotly_chart(fig_bar, use_container_width=True)

# =========================
# PIVOT TABLE
# =========================
st.subheader("📌 Tabela Dinâmica")

pivot = pd.pivot_table(
    df_filtrado,
    values="salario",
    index="cidade",
    columns="categoria_salario",
    aggfunc="mean"
)

st.dataframe(pivot)

# =========================
# DOWNLOAD
# =========================
st.subheader("⬇️ Download dos dados")

csv = df_filtrado.to_csv(index=False).encode("utf-8")
st.download_button(
    label="Baixar CSV",
    data=csv,
    file_name="dados_filtrados.csv",
    mime="text/csv"
)
