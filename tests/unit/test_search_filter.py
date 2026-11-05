import sqlite3
import pytest
from src.services.database import init_db
from src.services.seed import seed_initial_leaders
from src.services.member_service import strip_accents, create_member, list_members
from src.domain.models import MemberCreateRequest

def test_strip_accents():
    assert strip_accents("João") == "joao"
    assert strip_accents("Érika") == "erika"
    assert strip_accents("Ângela") == "angela"
    assert strip_accents("Núcleo") == "nucleo"
    assert strip_accents("Líder") == "lider"

def test_search_and_role_filtering():
    conn = sqlite3.connect(":memory:")
    conn.row_factory = sqlite3.Row
    init_db(conn)
    seed_initial_leaders(conn)

    user = {"id": 1, "name": "Pr. Pedro", "role": "Líder"}

    create_member(conn, MemberCreateRequest(name="João Victor", phone="(11) 91111-1111", birthDate="01/01/1990", position="Líder"), user)
    create_member(conn, MemberCreateRequest(name="Joana D'Arc", phone="(11) 92222-2222", birthDate="02/02/1992", position="Núcleo"), user)
    create_member(conn, MemberCreateRequest(name="Érika Santos", phone="(11) 93333-3333", birthDate="03/03/1993", position="Membro"), user)

    # Search 'joao' without accent matches 'João Victor'
    res1 = list_members(conn, search="joao")
    assert len(res1) == 1
    assert res1[0]["name"] == "João Victor"

    # Search 'erika' without accent matches 'Érika Santos'
    res2 = list_members(conn, search="erika")
    assert len(res2) == 1
    assert res2[0]["name"] == "Érika Santos"

    # Filter by position
    leaders = list_members(conn, position="Líder")
    assert len(leaders) == 1
    assert leaders[0]["name"] == "João Victor"

    nucleo = list_members(conn, position="Núcleo")
    assert len(nucleo) == 1
    assert nucleo[0]["name"] == "Joana D'Arc"

    conn.close()
