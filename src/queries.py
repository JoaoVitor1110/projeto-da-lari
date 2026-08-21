from datetime import date, datetime
from typing import Optional

import pandas as pd

from src.db import get_connection


def listar_filiais() -> pd.DataFrame:
    conn = get_connection()
    return pd.read_sql_query("SELECT id, nome FROM filiais ORDER BY nome", conn)


def grade_validacao(filial_id: int, data_ref: str) -> pd.DataFrame:
    """Retorna colaboradores da filial com o status de presenca na data_ref."""
    conn = get_connection()
    query = """
        SELECT
            c.id AS colaborador_id,
            c.nome AS colaborador,
            c.cargo,
            s.id AS setor_id,
            s.nome AS setor,
            COALESCE(p.status, 'pendente') AS status,
            p.hora_registro
        FROM colaboradores c
        JOIN setores s ON s.id = c.setor_id
        LEFT JOIN presencas p ON p.colaborador_id = c.id AND p.data = ?
        WHERE s.filial_id = ?
        ORDER BY s.nome, c.nome
    """
    return pd.read_sql_query(query, conn, params=(data_ref, filial_id))


def marcar_presenca(colaborador_id: int, data_ref: str, status: str) -> None:
    conn = get_connection()
    hora = datetime.now().strftime("%H:%M") if status == "presente" else None
    conn.execute(
        """INSERT INTO presencas (colaborador_id, data, status, hora_registro)
           VALUES (?, ?, ?, ?)
           ON CONFLICT(colaborador_id, data)
           DO UPDATE SET status = excluded.status, hora_registro = excluded.hora_registro""",
        (colaborador_id, data_ref, status, hora),
    )
    conn.commit()


def pendentes_todas_filiais(data_ref: str) -> pd.DataFrame:
    """Colaboradores ainda sem validacao (pendente) na data_ref, em todas as filiais."""
    conn = get_connection()
    query = """
        SELECT
            f.nome AS filial,
            s.nome AS setor,
            c.id AS colaborador_id,
            c.nome AS colaborador
        FROM colaboradores c
        JOIN setores s ON s.id = c.setor_id
        JOIN filiais f ON f.id = s.filial_id
        LEFT JOIN presencas p ON p.colaborador_id = c.id AND p.data = ?
        WHERE p.id IS NULL OR p.status = 'pendente'
        ORDER BY f.nome, s.nome, c.nome
    """
    return pd.read_sql_query(query, conn, params=(data_ref,))


def historico_presenca(dias: int = 7) -> pd.DataFrame:
    conn = get_connection()
    query = """
        SELECT
            p.data,
            f.nome AS filial,
            s.nome AS setor,
            p.status
        FROM presencas p
        JOIN colaboradores c ON c.id = p.colaborador_id
        JOIN setores s ON s.id = c.setor_id
        JOIN filiais f ON f.id = s.filial_id
        ORDER BY p.data DESC
        LIMIT 5000
    """
    df = pd.read_sql_query(query, conn)
    if df.empty:
        return df
    dias_recentes = sorted(df["data"].unique())[-dias:]
    return df[df["data"].isin(dias_recentes)]
