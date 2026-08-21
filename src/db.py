import os
import sqlite3
from datetime import date, timedelta

import streamlit as st

DATA_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data")
DB_PATH = os.path.join(DATA_DIR, "presenca.db")

SCHEMA = """
CREATE TABLE IF NOT EXISTS filiais (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nome TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS setores (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    filial_id INTEGER NOT NULL REFERENCES filiais(id),
    nome TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS colaboradores (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    setor_id INTEGER NOT NULL REFERENCES setores(id),
    nome TEXT NOT NULL,
    cargo TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS presencas (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    colaborador_id INTEGER NOT NULL REFERENCES colaboradores(id),
    data TEXT NOT NULL,
    status TEXT NOT NULL DEFAULT 'pendente',
    hora_registro TEXT,
    UNIQUE(colaborador_id, data)
);
"""

FILIAIS = ["Filial Centro", "Filial Shopping Norte", "Filial Zona Sul"]

SETORES_POR_FILIAL = ["Bilheteria", "Bomboniere", "Projecao", "Limpeza", "Gerencia"]

NOMES = [
    "Ana Silva", "Bruno Costa", "Carla Souza", "Diego Lima", "Elisa Rocha",
    "Fabio Alves", "Gabriela Dias", "Hugo Martins", "Isabela Nunes", "Joao Pereira",
    "Karina Melo", "Lucas Barros", "Mariana Teixeira", "Nicolas Ferreira", "Otavio Ramos",
    "Patricia Gomes", "Rafael Cardoso", "Sabrina Pinto", "Thiago Moreira", "Vanessa Castro",
    "William Duarte", "Yasmin Correia", "Zeca Andrade", "Aline Freitas", "Bernardo Vieira",
    "Camila Rezende", "Daniel Xavier", "Eduarda Farias", "Felipe Guedes", "Giovana Lopes",
]

CARGOS = ["Atendente", "Operador", "Supervisor", "Auxiliar"]


@st.cache_resource
def get_connection() -> sqlite3.Connection:
    os.makedirs(DATA_DIR, exist_ok=True)
    conn = sqlite3.connect(DB_PATH, check_same_thread=False)
    conn.execute("PRAGMA foreign_keys = ON")
    conn.executescript(SCHEMA)
    conn.commit()
    _seed_if_empty(conn)
    return conn


def _seed_if_empty(conn: sqlite3.Connection) -> None:
    cur = conn.execute("SELECT COUNT(*) FROM filiais")
    if cur.fetchone()[0] > 0:
        return

    nome_iter = iter(NOMES)
    for filial_nome in FILIAIS:
        filial_id = conn.execute(
            "INSERT INTO filiais (nome) VALUES (?)", (filial_nome,)
        ).lastrowid
        for setor_nome in SETORES_POR_FILIAL:
            setor_id = conn.execute(
                "INSERT INTO setores (filial_id, nome) VALUES (?, ?)",
                (filial_id, setor_nome),
            ).lastrowid
            for i in range(2):
                try:
                    nome = next(nome_iter)
                except StopIteration:
                    nome_iter = iter(NOMES)
                    nome = next(nome_iter)
                cargo = CARGOS[i % len(CARGOS)]
                conn.execute(
                    "INSERT INTO colaboradores (setor_id, nome, cargo) VALUES (?, ?, ?)",
                    (setor_id, nome, cargo),
                )
    conn.commit()
    _seed_historico(conn)


def _seed_historico(conn: sqlite3.Connection) -> None:
    """Gera historico de presenca dos ultimos 7 dias para alimentar o dashboard."""
    import random

    random.seed(42)
    colaboradores = conn.execute("SELECT id FROM colaboradores").fetchall()
    today = date.today()
    for offset in range(7, 0, -1):
        dia = (today - timedelta(days=offset)).isoformat()
        for (colaborador_id,) in colaboradores:
            status = "presente" if random.random() < 0.85 else "ausente"
            hora = f"{random.randint(7, 9):02d}:{random.randint(0, 59):02d}" if status == "presente" else None
            conn.execute(
                """INSERT OR IGNORE INTO presencas (colaborador_id, data, status, hora_registro)
                   VALUES (?, ?, ?, ?)""",
                (colaborador_id, dia, status, hora),
            )
    conn.commit()
