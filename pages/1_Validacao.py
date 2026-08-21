from datetime import date

import pandas as pd
import streamlit as st

from src.queries import ausentes_todas_filiais, grade_validacao, listar_filiais, marcar_presenca
from src.style import STATUS_STYLE, inject

st.set_page_config(page_title="Validacao de Presenca", page_icon="✅", layout="wide")
inject(st)

st.markdown('<span class="bp-eyebrow">Planta &middot; Controle de presenca</span>', unsafe_allow_html=True)
st.title("✅ Validacao de Presenca")
st.caption(
    "Cada cadeira representa um vendedor — todos comecam o dia marcados como presentes. "
    "Clique na cadeira de quem **nao veio** para desmarcar."
)

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

m1, m2, m3 = st.columns(3)
m1.metric("Total de cadeiras", total)
m2.metric("🟢 Presentes", presentes)
m3.metric("⚪ Ausentes (desmarcados)", ausentes)

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
        colunas = st.columns(4)
        legenda_linhas = []
        for numero, (_, linha) in enumerate(grupo.iterrows(), start=1):
            estilo = STATUS_STYLE[linha["status"]]
            legenda_linhas.append(f"<b>{numero}</b> = {linha['colaborador']}")
            with colunas[(numero - 1) % 4]:
                with st.container(border=True):
                    st.markdown(
                        f"<div class='bp-seat-num' style=\"background:{estilo['cor']}22;"
                        f"color:{estilo['cor']};border:2px solid {estilo['cor']}\">{numero}</div>",
                        unsafe_allow_html=True,
                    )
                    st.markdown(
                        f"<div style='text-align:center'>"
                        f"<span class='bp-desk-role'>{linha['cargo']}</span></div>",
                        unsafe_allow_html=True,
                    )
                    hora = (
                        f" <span style='color:#9AA0AA;font-size:0.72em'>({linha['hora_registro']})</span>"
                        if pd.notna(linha["hora_registro"]) else ""
                    )
                    st.markdown(
                        f"<div style='text-align:center'><span class='bp-badge' "
                        f"style=\"background:{estilo['cor']}22;color:{estilo['cor']};"
                        f"border:1px solid {estilo['cor']}55\">{estilo['icone']} {estilo['label']}</span>{hora}</div>",
                        unsafe_allow_html=True,
                    )
                    if linha["status"] == "presente":
                        if st.button("Desmarcar (faltou)", key=f"toggle_{linha['colaborador_id']}", width="stretch"):
                            marcar_presenca(int(linha["colaborador_id"]), data_ref_str, "ausente")
                            st.rerun()
                    else:
                        if st.button("Marcar presente", key=f"toggle_{linha['colaborador_id']}", width="stretch"):
                            marcar_presenca(int(linha["colaborador_id"]), data_ref_str, "presente")
                            st.rerun()
        st.markdown(
            f"<div class='bp-legend-list'>{' &nbsp;&middot;&nbsp; '.join(legenda_linhas)}</div>",
            unsafe_allow_html=True,
        )
        st.markdown("</div>", unsafe_allow_html=True)

with col_sidebar:
    st.markdown('<span class="bp-eyebrow">Legenda de status</span>', unsafe_allow_html=True)
    for chave, estilo in STATUS_STYLE.items():
        st.markdown(
            f"<span class='bp-badge' style=\"background:{estilo['cor']}22;color:{estilo['cor']};"
            f"border:1px solid {estilo['cor']}55\">{estilo['icone']} {estilo['label']}</span>",
            unsafe_allow_html=True,
        )
    st.markdown("")

    aus_df = ausentes_todas_filiais(data_ref_str)
    st.markdown(
        f'<span class="bp-eyebrow">Painel de avisos — faltas em todas as filiais ({len(aus_df)})</span>',
        unsafe_allow_html=True,
    )
    if aus_df.empty:
        st.markdown(
            "<div class='bp-aviso'><span class='what'>Ninguem foi desmarcado ainda hoje.</span></div>",
            unsafe_allow_html=True,
        )
    else:
        for _, row in aus_df.head(15).iterrows():
            st.markdown(
                f"""<div class="bp-aviso">
                    <span class="who">{row['colaborador']}</span><br>
                    <span class="what">{row['filial']} · {row['setor']} — nao veio hoje</span>
                    </div>""",
                unsafe_allow_html=True,
            )
        if len(aus_df) > 15:
            st.caption(f"+ {len(aus_df) - 15} outras faltas...")

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
