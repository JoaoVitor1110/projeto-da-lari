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

- **Validacao** — mapa visual por setor (estilo planta baixa), separado por filial. Cada cadeira
  numerada representa um vendedor (legenda abaixo mostra quem e quem) e comeca o dia marcada
  como presente — o gestor so precisa desmarcar quem nao veio. Um painel lateral mostra as
  faltas de todas as filiais. Emita o relatorio do dia ao final.
- **Dashboard** — visao consolidada de presenca por filial, setor e nos ultimos dias.

Este e um protótipo com dados fictícios para validação do conceito com o gestor.
    """
)
