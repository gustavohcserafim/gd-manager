import os
import sqlite3
import tempfile
from pathlib import Path

def get_default_db_path() -> str:
    env_path = os.environ.get("GD_DB_PATH")
    if env_path:
        return env_path
    temp_dir = tempfile.gettempdir()
    return str(Path(temp_dir) / "gd_manager.db")

def get_db_path() -> str:
    return os.environ.get("GD_DB_PATH", get_default_db_path())

def get_db_connection() -> sqlite3.Connection:
    db_path = get_db_path()
    conn = sqlite3.connect(db_path, check_same_thread=False)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON;")
    return conn

def init_db(conn: sqlite3.Connection) -> None:
    """Initializes tables and indexes per the data model."""
    conn.execute("PRAGMA foreign_keys = ON;")
    cursor = conn.cursor()

    cursor.executescript("""
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        pin_hash TEXT NOT NULL,
        role TEXT NOT NULL CHECK(role IN ('Líder', 'Núcleo')),
        active INTEGER NOT NULL DEFAULT 1,
        created_at TEXT NOT NULL
    );

    CREATE INDEX IF NOT EXISTS idx_users_active ON users(active);

    CREATE TABLE IF NOT EXISTS members (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        phone TEXT NOT NULL UNIQUE,
        phone_formatted TEXT NOT NULL,
        birth_date TEXT NOT NULL,
        birth_day INTEGER NOT NULL,
        birth_month INTEGER NOT NULL,
        birth_year INTEGER,
        position TEXT NOT NULL CHECK(position IN ('Líder', 'Núcleo', 'Membro')),
        created_by_user_id INTEGER NOT NULL REFERENCES users(id),
        updated_by_user_id INTEGER NOT NULL REFERENCES users(id),
        created_at TEXT NOT NULL,
        updated_at TEXT NOT NULL
    );

    CREATE UNIQUE INDEX IF NOT EXISTS idx_members_phone_unique ON members(phone);
    CREATE INDEX IF NOT EXISTS idx_members_name ON members(name COLLATE NOCASE);
    CREATE INDEX IF NOT EXISTS idx_members_position ON members(position);
    CREATE INDEX IF NOT EXISTS idx_members_birthday ON members(birth_month, birth_day);

    CREATE TABLE IF NOT EXISTS activity_logs (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER NOT NULL REFERENCES users(id),
        user_name TEXT NOT NULL,
        action_type TEXT NOT NULL CHECK(action_type IN ('CREATE_MEMBER', 'UPDATE_MEMBER', 'DELETE_MEMBER')),
        member_id INTEGER,
        member_name TEXT NOT NULL,
        details TEXT,
        created_at TEXT NOT NULL
    );

    CREATE INDEX IF NOT EXISTS idx_logs_created_at_desc ON activity_logs(created_at DESC);
    CREATE INDEX IF NOT EXISTS idx_logs_user_id ON activity_logs(user_id);
    """)
    conn.commit()
