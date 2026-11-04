import sqlite3
from typing import Optional


def get_connection(db_path: str = "gd_manager.db") -> sqlite3.Connection:
    """Cria e retorna uma conexão com SQLite configurada para row_factory e foreign keys."""
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON;")
    return conn


def init_db(db_path: str = "gd_manager.db", conn: Optional[sqlite3.Connection] = None) -> None:
    """Inicializa as tabelas e índices necessários no SQLite conforme o data-model.md."""
    should_close = False
    if conn is None:
        conn = get_connection(db_path)
        should_close = True

    try:
        with conn:
            conn.execute("""
                CREATE TABLE IF NOT EXISTS members (
                    id TEXT PRIMARY KEY,
                    name TEXT NOT NULL,
                    phone TEXT NOT NULL,
                    email TEXT,
                    role TEXT NOT NULL CHECK (role IN ('leader', 'core', 'normal')),
                    status TEXT NOT NULL CHECK (status IN ('active', 'inactive')),
                    created_at TEXT NOT NULL,
                    updated_at TEXT NOT NULL
                );
            """)

            conn.execute("""
                CREATE INDEX IF NOT EXISTS idx_members_name ON members(name COLLATE NOCASE);
            """)

            conn.execute("""
                CREATE INDEX IF NOT EXISTS idx_members_status_role ON members(status, role);
            """)

            conn.execute("""
                CREATE UNIQUE INDEX IF NOT EXISTS idx_members_active_phone 
                ON members(phone) 
                WHERE status = 'active';
            """)
    finally:
        if should_close:
            conn.close()
