import sys
from pathlib import Path

# Adiciona o diretório backend e o root do projeto ao sys.path para importações de 'src' e 'backend'
backend_dir = Path(__file__).resolve().parent.parent
project_root = backend_dir.parent
for path in (str(backend_dir), str(project_root)):
    if path not in sys.path:
        sys.path.insert(0, path)

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
