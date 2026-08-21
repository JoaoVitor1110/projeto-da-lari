# Controle de Presenca 🧭

Prototipo de painel para o gestor validar quem veio trabalhar / quem esta
online, com visao por filial e setor, em estilo "planta baixa" (navy/cyan,
fontes IBM Plex) — visual adaptado do mockup inicial de referencia
(`Painel de Mesas`).

## Funcionalidades (MVP)

- **Validacao** (`pages/1_Validacao.py`): mapa por setor (cada setor vira
  uma "sala" com cantos tracejados), colaboradores como cartoes com status
  colorido (🟢 presente / 🔴 ausente / ⚪ pendente). O gestor clica para
  marcar presenca do dia. Painel lateral "avisos" lista as pendencias de
  **todas** as filiais, nao so a selecionada. Botao para emitir o
  relatorio do dia em CSV.
- **Dashboard** (`pages/2_Dashboard.py`): metricas e graficos de presenca
  por filial e setor, alem da evolucao da taxa de presenca nos ultimos dias.
- Dados de exemplo (3 filiais, 5 setores cada, 30 colaboradores e historico
  de 7 dias) sao gerados automaticamente no primeiro uso, em SQLite local.
- `src/style.py` concentra o tema visual (cores, fontes, CSS do estilo
  "planta baixa") para manter consistencia entre as paginas.

## Como rodar localmente

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
streamlit run app.py
```

O app abre em `http://localhost:8501`. O banco (`data/presenca.db`) e
criado e populado com dados ficticios automaticamente.

Para recomecar do zero, apague `data/presenca.db` e rode novamente.

## Estrutura

```
app.py                  # pagina inicial
pages/1_Validacao.py    # tela de validacao (mapa visual + relatorio)
pages/2_Dashboard.py    # dashboard de presenca
src/db.py               # schema, conexao e seed do SQLite
src/queries.py          # leitura/escrita de presenca
.streamlit/config.toml  # tema visual
```

## Status: prototipo para validacao com o gestor

Este e um MVP com dados ficticios, pensado para apresentar o **conceito
visual** e o fluxo de uso. Antes de ir para producao ainda faltam, entre
outros pontos:

- Login/autenticacao do gestor (por filial)
- Cadastro real de filiais, setores e colaboradores (hoje e via seed)
- Definir o mecanismo real de presenca: o proprio colaborador faz check-in
  (ex. QR code / app) ou o gestor marca manualmente (como neste prototipo)
- Relatorio em PDF, alem do CSV
- Banco de dados compartilhado (Postgres) se houver mais de um gestor
  usando ao mesmo tempo
- Deploy (Streamlit Community Cloud, Docker, servidor proprio)
