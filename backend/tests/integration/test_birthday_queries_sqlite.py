from datetime import date, timedelta
import sqlite3
import pytest
from src.infrastructure.database.connection import init_db
from src.domain.entities.member import Member
from src.domain.enums.member_enums import MemberRole
from src.infrastructure.database.sqlite_member_repository import SqliteMemberRepository


def test_schema_migration_adds_birth_date_to_existing_legacy_table():
    # Cria uma base em memória simulando o esquema legado da Feature 001 (sem birth_date)
    conn = sqlite3.connect(":memory:")
    conn.row_factory = sqlite3.Row
    with conn:
        conn.execute("""
            CREATE TABLE members (
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
            INSERT INTO members (id, name, phone, email, role, status, created_at, updated_at)
            VALUES ('m-legacy-1', 'Membro Antigo', '11999990000', 'antigo@gd.org', 'normal', 'active', '2026-01-01T00:00:00', '2026-01-01T00:00:00');
        """)

    # Executa a migração via init_db
    init_db(conn=conn)

    # Verifica se a coluna birth_date agora existe
    cursor = conn.execute("PRAGMA table_info(members);")
    columns = [row["name"] for row in cursor.fetchall()]
    assert "birth_date" in columns

    # Verifica se o índice idx_members_birth_date foi criado
    cursor = conn.execute("PRAGMA index_list(members);")
    indexes = [row["name"] for row in cursor.fetchall()]
    assert "idx_members_birth_date" in indexes

    # Verifica se o registro legado permanece intacto com birth_date NULL
    cursor = conn.execute("SELECT id, name, birth_date FROM members WHERE id = 'm-legacy-1';")
    row = cursor.fetchone()
    assert row["id"] == "m-legacy-1"
    assert row["name"] == "Membro Antigo"
    assert row["birth_date"] is None

    conn.close()


def test_fresh_db_has_birth_date_column_and_index():
    conn = sqlite3.connect(":memory:")
    conn.row_factory = sqlite3.Row
    init_db(conn=conn)

    cursor = conn.execute("PRAGMA table_info(members);")
    columns = [row["name"] for row in cursor.fetchall()]
    assert "birth_date" in columns

    cursor = conn.execute("PRAGMA index_list(members);")
    indexes = [row["name"] for row in cursor.fetchall()]
    assert "idx_members_birth_date" in indexes

    conn.close()


def test_sqlite_create_and_find_with_birth_date(memory_db):
    repo = SqliteMemberRepository(memory_db)
    m = Member.create(
        name="Juliana Lima",
        phone="11977776666",
        role=MemberRole.CORE,
        birth_date=date(1994, 8, 25),
    )
    repo.create(m)

    found = repo.find_by_id(m.id)
    assert found is not None
    assert found.birth_date == date(1994, 8, 25)

    all_members = repo.find_all()
    assert any(x.id == m.id and x.birth_date == date(1994, 8, 25) for x in all_members)


def test_sqlite_update_birth_date(memory_db):
    repo = SqliteMemberRepository(memory_db)
    m = Member.create(
        name="Juliana Lima",
        phone="11977776666",
        role=MemberRole.CORE,
        birth_date=date(1994, 8, 25),
    )
    repo.create(m)

    m.update_info(
        name="Juliana Lima Santos",
        phone="11977776666",
        email=None,
        role=MemberRole.CORE,
        birth_date=date(1994, 8, 26),
    )
    repo.update(m)

    updated = repo.find_by_id(m.id)
    assert updated is not None
    assert updated.birth_date == date(1994, 8, 26)


def test_sqlite_find_all_filtered_by_birthday_month(memory_db):
    repo = SqliteMemberRepository(memory_db)
    m1 = Member.create(name="Member Maio 1", phone="11911110001", birth_date=date(1990, 5, 12))
    m2 = Member.create(name="Member Maio 2", phone="11911110002", birth_date=date(1993, 5, 30))
    m3 = Member.create(name="Member Junho", phone="11911110003", birth_date=date(1991, 6, 1))
    repo.create(m1)
    repo.create(m2)
    repo.create(m3)

    may_list = repo.find_all(birthday_month=5)
    assert len(may_list) == 2
    assert {m.name for m in may_list} == {"Member Maio 1", "Member Maio 2"}

    june_list = repo.find_all(birthday_month=6)
    assert len(june_list) == 1
    assert june_list[0].name == "Member Junho"


def test_sqlite_find_upcoming_birthdays(memory_db):
    repo = SqliteMemberRepository(memory_db)
    today = date.today()
    # Aniversariante amanhã
    bday_tomorrow = today + timedelta(days=1)
    m_tomorrow = Member.create(name="Amanhã", phone="11922220001", birth_date=date(1992, bday_tomorrow.month, bday_tomorrow.day))

    # Aniversariante hoje
    m_today = Member.create(name="Hoje", phone="11922220002", birth_date=date(1990, today.month, today.day))

    # Aniversariante daqui a 60 dias (fora da janela)
    bday_60 = today + timedelta(days=60)
    m_far = Member.create(name="Distante", phone="11922220003", birth_date=date(1995, bday_60.month, bday_60.day))

    repo.create(m_tomorrow)
    repo.create(m_today)
    repo.create(m_far)

    upcoming = repo.find_upcoming_birthdays(days=30)
    assert len(upcoming) == 2
    assert upcoming[0].id == m_today.id
    assert upcoming[1].id == m_tomorrow.id


