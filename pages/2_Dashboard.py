import pandas as pd
import plotly.express as px
import streamlit as st

from src.queries import historico_presenca
from src.style import inject

st.set_page_config(page_title="Dashboard de Presenca", page_icon="📊", layout="wide")
inject(st)

st.markdown('<span class="bp-eyebrow">Planta &middot; Controle de presenca</span>', unsafe_allow_html=True)
st.title("📊 Dashboard de Presenca")
st.caption("Visao consolidada de presenca por filial, setor e periodo.")

df = historico_presenca(dias=7)

if df.empty:
    st.info("Ainda nao ha dados de presenca registrados.")
    st.stop()

filiais_sel = st.multiselect(
    "Filiais", sorted(df["filial"].unique()), default=sorted(df["filial"].unique())
)
df = df[df["filial"].isin(filiais_sel)]

hoje = df["data"].max()
df_hoje = df[df["data"] == hoje]

total = len(df_hoje)
presentes = (df_hoje["status"] == "presente").sum()
ausentes = (df_hoje["status"] == "ausente").sum()
taxa = (presentes / total * 100) if total else 0

c1, c2, c3, c4 = st.columns(4)
c1.metric("Colaboradores (hoje)", total)
c2.metric("🟢 Presentes", presentes)
c3.metric("⚪ Ausentes", ausentes)
c4.metric("Taxa de presenca", f"{taxa:.0f}%")

st.divider()

col1, col2 = st.columns(2)

with col1:
    st.subheader("Presenca por filial (hoje)")
    por_filial = (
        df_hoje.groupby(["filial", "status"]).size().reset_index(name="qtd")
    )
    fig = px.bar(
        por_filial, x="filial", y="qtd", color="status",
        color_discrete_map={"presente": "#34D399", "ausente": "#64748B"},
        barmode="stack", labels={"filial": "Filial", "qtd": "Colaboradores", "status": "Status"},
    )
    st.plotly_chart(fig, width='stretch')

with col2:
    st.subheader("Presenca por setor (hoje)")
    por_setor = df_hoje.groupby(["setor", "status"]).size().reset_index(name="qtd")
    fig2 = px.bar(
        por_setor, x="setor", y="qtd", color="status",
        color_discrete_map={"presente": "#34D399", "ausente": "#64748B"},
        barmode="stack", labels={"setor": "Setor", "qtd": "Colaboradores", "status": "Status"},
    )
    st.plotly_chart(fig2, width='stretch')

st.subheader("Evolucao da taxa de presenca (ultimos dias)")
evolucao = (
    df.groupby(["data", "status"]).size().reset_index(name="qtd")
    .pivot(index="data", columns="status", values="qtd").fillna(0)
)
for col in ["presente", "ausente"]:
    if col not in evolucao:
        evolucao[col] = 0
evolucao["taxa_presenca"] = evolucao["presente"] / (evolucao["presente"] + evolucao["ausente"]) * 100
fig3 = px.line(
    evolucao.reset_index(), x="data", y="taxa_presenca", markers=True,
    labels={"data": "Data", "taxa_presenca": "Taxa de presenca (%)"},
)
fig3.update_traces(line_color="#4FD1E8")
st.plotly_chart(fig3, width='stretch')
