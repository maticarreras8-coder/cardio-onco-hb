import sqlite3
from pathlib import Path

from config.settings import DB_PATH


def get_connection():
    db_file = Path(DB_PATH)
    db_file.parent.mkdir(parents=True, exist_ok=True)

    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def _column_exists(conn, table_name: str, column_name: str) -> bool:
    cur = conn.cursor()
    cur.execute(f"PRAGMA table_info({table_name})")
    columns = [row["name"] for row in cur.fetchall()]
    return column_name in columns


def _add_column_if_missing(conn, table_name: str, column_name: str, column_def: str):
    if not _column_exists(conn, table_name, column_name):
        conn.execute(f"ALTER TABLE {table_name} ADD COLUMN {column_name} {column_def}")


def init_db():
    conn = get_connection()
    schema_path = Path("data/schema.sql")

    with open(schema_path, "r", encoding="utf-8") as f:
        schema_sql = f.read()

    conn.executescript(schema_sql)

    # Migraciones suaves para prototipo
    _add_column_if_missing(conn, "visits", "symptomatic_or_functional_limitation", "INTEGER DEFAULT 0")
    _add_column_if_missing(conn, "visits", "troponin_basal", "REAL")
    _add_column_if_missing(conn, "visits", "bnp_ntprobnp_basal", "REAL")
    _add_column_if_missing(conn, "visits", "cpet_performed", "INTEGER DEFAULT 0")
    _add_column_if_missing(conn, "visits", "cpet_vo2_peak", "REAL")
    _add_column_if_missing(conn, "visits", "cpet_percent_predicted", "REAL")
    _add_column_if_missing(conn, "visits", "cpet_interpretation", "TEXT")

    conn.commit()
    conn.close()
