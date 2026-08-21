from datetime import date

import pandas as pd
import streamlit as st

from src.queries import grade_validacao, listar_filiais, marcar_presenca, pendentes_todas_filiais
from src.style import STATUS_STYLE, inject

st.set_page_config(page_title="Validacao de Presenca", page_icon="✅", layout="wide")
inject(st)

st.markdown('<span class="bp-eyebrow">Planta &middot; Controle de presenca</span>', unsafe_allow_html=True)
st.title("✅ Validacao de Presenca")
st.caption("Mapa por setor — clique em presente/ausente para validar cada colaborador.")

filiais_df = listar_filiais()
col_a, col_b = st.columns([2, 1])
with col_a:
    filial_nome = st.selectbox("Filial", filiais_df["nome"])
with col_b:
    data_ref = st.date_input("Data", value=date.today())

filial_id = int(filiais_df.loc[filiais_df["nome"] == filial_nome, "id"].iloc[0])
data_ref_str = data_ref.isoformat()

df = grade_validacao(filial_id, data_ref_str)

if df.empty:
    st.info("Nenhum colaborador cadastrado para esta filial.")
    st.stop()

total = len(df)
presentes = (df["status"] == "presente").sum()
ausentes = (df["status"] == "ausente").sum()
pendentes = (df["status"] == "pendente").sum()

m1, m2, m3, m4 = st.columns(4)
m1.metric("Total", total)
m2.metric("🟢 Presentes", presentes)
m3.metric("🔴 Ausentes", ausentes)
m4.metric("⚪ Pendentes", pendentes)

st.divider()

col_floor, col_sidebar = st.columns([3, 1], gap="large")

with col_floor:
    for setor_nome, grupo in df.groupby("setor", sort=True):
        st.markdown(
            f"""
            <div class="bp-room">
              <span class="bp-room-label">{setor_nome} — setor</span>
              <span class="bp-tick tl"></span><span class="bp-tick tr"></span>
              <span class="bp-tick bl"></span><span class="bp-tick br"></span>
            """,
            unsafe_allow_html=True,
        )
        colunas = st.columns(3)
        for idx, (_, linha) in enumerate(grupo.iterrows()):
            estilo = STATUS_STYLE[linha["status"]]
            with colunas[idx % 3]:
                with st.container(border=True):
                    pendente_dot = (
                        '<span class="bp-pending-dot"></span>' if linha["status"] == "pendente" else ""
                    )
                    st.markdown(
                        f"{pendente_dot}<span class='bp-desk-name'>{linha['colaborador']}</span><br>"
                        f"<span class='bp-desk-role'>{linha['cargo']}</span>",
                        unsafe_allow_html=True,
                    )
                    hora = (
                        f" <span style='color:#9AA0AA;font-size:0.75em'>({linha['hora_registro']})</span>"
                        if pd.notna(linha["hora_registro"]) else ""
                    )
                    st.markdown(
                        f"<span class='bp-badge' style=\"background:{estilo['cor']}22;"
                        f"color:{estilo['cor']};border:1px solid {estilo['cor']}55\">"
                        f"{estilo['icone']} {estilo['label']}</span>{hora}",
                        unsafe_allow_html=True,
                    )
                    b1, b2 = st.columns(2)
                    if b1.button("🟢 Veio", key=f"presente_{linha['colaborador_id']}", width="stretch"):
                        marcar_presenca(int(linha["colaborador_id"]), data_ref_str, "presente")
                        st.rerun()
                    if b2.button("🔴 Faltou", key=f"ausente_{linha['colaborador_id']}", width="stretch"):
                        marcar_presenca(int(linha["colaborador_id"]), data_ref_str, "ausente")
                        st.rerun()
        st.markdown("</div>", unsafe_allow_html=True)

with col_sidebar:
    st.markdown('<span class="bp-eyebrow">Legenda</span>', unsafe_allow_html=True)
    for chave, estilo in STATUS_STYLE.items():
        st.markdown(
            f"<span class='bp-badge' style=\"background:{estilo['cor']}22;color:{estilo['cor']};"
            f"border:1px solid {estilo['cor']}55\">{estilo['icone']} {estilo['label']}</span>",
            unsafe_allow_html=True,
        )
    st.markdown("")

    pend_df = pendentes_todas_filiais(data_ref_str)
    st.markdown(
        f'<span class="bp-eyebrow">Painel de avisos — todas as filiais ({len(pend_df)})</span>',
        unsafe_allow_html=True,
    )
    if pend_df.empty:
        st.markdown(
            "<div class='bp-aviso'><span class='what'>Nenhuma pendencia — todos validados hoje.</span></div>",
            unsafe_allow_html=True,
        )
    else:
        for _, row in pend_df.head(15).iterrows():
            st.markdown(
                f"""<div class="bp-aviso">
                    <span class="who">{row['colaborador']}</span><br>
                    <span class="what">{row['filial']} · {row['setor']} — pendente de validacao</span>
                    </div>""",
                unsafe_allow_html=True,
            )
        if len(pend_df) > 15:
            st.caption(f"+ {len(pend_df) - 15} outras pendencias...")

st.divider()

st.subheader("📄 Relatorio do dia")
relatorio = df[["setor", "colaborador", "cargo", "status", "hora_registro"]].rename(
    columns={
        "setor": "Setor",
        "colaborador": "Colaborador",
        "cargo": "Cargo",
        "status": "Status",
        "hora_registro": "Hora do registro",
    }
)
csv_bytes = relatorio.to_csv(index=False).encode("utf-8-sig")

st.download_button(
    label="⬇️ Emitir relatorio do dia (CSV)",
    data=csv_bytes,
    file_name=f"relatorio_presenca_{filial_nome.replace(' ', '_')}_{data_ref_str}.csv",
    mime="text/csv",
    type="primary",
)

with st.expander("Ver tabela completa"):
    st.dataframe(relatorio, width="stretch", hide_index=True)
