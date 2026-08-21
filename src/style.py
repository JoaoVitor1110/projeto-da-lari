STATUS_STYLE = {
    "presente": {"cor": "#34D399", "label": "Presente", "icone": "🟢"},
    "ausente": {"cor": "#FB7185", "label": "Ausente", "icone": "🔴"},
    "pendente": {"cor": "#64748B", "label": "Pendente", "icone": "⚪"},
}

BLUEPRINT_CSS = """
<link rel="preconnect" href="https://fonts.googleapis.com">
<link href="https://fonts.googleapis.com/css2?family=IBM+Plex+Mono:wght@400;500;600;700&family=IBM+Plex+Sans:wght@400;500;600;700&display=swap" rel="stylesheet">
<style>
:root{
  --navy:#0F2A4A;
  --navy-deep:#091b30;
  --panel:#15335c;
  --panel-hi:#1c4173;
  --line: rgba(140,185,230,0.22);
  --line-strong: rgba(140,185,230,0.4);
  --ink:#EAF2FB;
  --muted:#9FB8D9;
  --cyan:#4FD1E8;
  --ok:#34D399;
  --ferias:#FBBF24;
  --atestado:#FB7185;
  --inativo:#64748B;
}
html, body, [class*="css"] { font-family:'IBM Plex Sans', system-ui, sans-serif; }
.stApp {
  background-color: var(--navy);
  background-image:
    linear-gradient(var(--line) 1px, transparent 1px),
    linear-gradient(90deg, var(--line) 1px, transparent 1px);
  background-size: 28px 28px;
}
.bp-eyebrow{
  font-family:'IBM Plex Mono', monospace; font-size:11px; letter-spacing:0.14em;
  color:var(--cyan); text-transform:uppercase;
}
.bp-room{
  position:relative;
  border:1.5px dashed var(--line-strong);
  border-radius:6px;
  padding:26px 18px 14px 18px;
  margin-bottom:22px;
}
.bp-room-label{
  position:absolute; top:-11px; left:14px; background:var(--navy);
  padding:0 8px; font-family:'IBM Plex Mono', monospace; font-size:11px;
  letter-spacing:0.08em; color:var(--muted); text-transform:uppercase;
}
.bp-tick{ position:absolute; width:12px; height:12px; border-color:var(--cyan); border-style:solid; opacity:0.85; }
.bp-tick.tl{ top:-1px; left:-1px; border-width:2px 0 0 2px; }
.bp-tick.tr{ top:-1px; right:-1px; border-width:2px 2px 0 0; }
.bp-tick.bl{ bottom:-1px; left:-1px; border-width:0 0 2px 2px; }
.bp-tick.br{ bottom:-1px; right:-1px; border-width:0 2px 2px 0; }

.bp-desk-name{ font-size:13px; font-weight:600; color:var(--ink); }
.bp-desk-role{ font-size:11.5px; color:var(--muted); }
.bp-badge{
  font-family:'IBM Plex Mono', monospace; font-size:10px; letter-spacing:0.05em;
  text-transform:uppercase; padding:2px 8px; border-radius:20px; display:inline-block;
}
.bp-pending-dot{
  display:inline-block; width:8px; height:8px; border-radius:50%;
  background:var(--atestado); margin-right:6px;
  box-shadow:0 0 0 2px rgba(251,113,133,0.25);
}
.bp-aviso{
  background:var(--panel); border:1px solid var(--line-strong); border-left:3px solid var(--atestado);
  border-radius:6px; padding:8px 10px; font-size:12.5px; margin-bottom:8px;
}
.bp-aviso .who{ font-weight:600; color:var(--ink); }
.bp-aviso .what{ color:var(--muted); font-size:11px; }
</style>
<style>
div[data-testid="stVerticalBlockBorderWrapper"] { background: var(--panel); border-radius: 8px; }
</style>
"""


def inject(st) -> None:
    st.markdown(BLUEPRINT_CSS, unsafe_allow_html=True)
