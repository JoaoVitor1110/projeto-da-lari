import streamlit as st

from src.style import inject

st.set_page_config(
    page_title="Controle de Presenca",
    page_icon="🧭",
    layout="wide",
)
inject(st)

st.markdown('<span class="bp-eyebrow">Planta &middot; Controle de presenca</span>', unsafe_allow_html=True)
st.title("🧭 Controle de Presenca")
st.caption("Painel do gestor para validar quem veio trabalhar, por filial e setor.")

st.markdown(
    """
Use o menu lateral para navegar:

- **Validacao** — mapa visual dos colaboradores por setor (estilo planta baixa), separados por filial.
  Clique em presente/ausente para validar. Um painel lateral mostra as pendencias de todas as filiais.
  Emita o relatorio do dia ao final.
- **Dashboard** — visao consolidada de presenca por filial, setor e nos ultimos dias.

Este e um protótipo com dados fictícios para validação do conceito com o gestor.
    """
)
