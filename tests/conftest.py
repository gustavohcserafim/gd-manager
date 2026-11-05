import os
import sqlite3
import tempfile
from pathlib import Path
import pytest

TEST_DB_PATH = str(Path(tempfile.gettempdir()) / "gd_test_suite.db")
os.environ["GD_ENV"] = "test"
os.environ["GD_DB_PATH"] = TEST_DB_PATH

from src.services.database import init_db, get_db_connection
from src.services.seed import seed_initial_leaders

@pytest.fixture(autouse=True)
def clean_test_db():
    """Initializes a fresh schema and seed data in the test database for each test."""
    conn = get_db_connection()
    # Clean tables if existing
    cursor = conn.cursor()
    cursor.executescript("""
        DROP TABLE IF EXISTS activity_logs;
        DROP TABLE IF EXISTS members;
        DROP TABLE IF EXISTS users;
    """)
    conn.commit()
    init_db(conn)
    seed_initial_leaders(conn)
    conn.close()
    yield
