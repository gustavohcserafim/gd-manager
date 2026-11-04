import sys
from pathlib import Path

# Adiciona o diretório backend ao sys.path para importações diretas de 'src'
backend_dir = Path(__file__).resolve().parent.parent
if str(backend_dir) not in sys.path:
    sys.path.insert(0, str(backend_dir))

import pytest
import sqlite3
from src.infrastructure.database.connection import init_db


@pytest.fixture
def memory_db() -> sqlite3.Connection:
    """Fixture que fornece uma conexão isolada com SQLite em memória (:memory:) já inicializada."""
    conn = sqlite3.connect(":memory:")
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON;")
    init_db(conn=conn)
    yield conn
    conn.close()
