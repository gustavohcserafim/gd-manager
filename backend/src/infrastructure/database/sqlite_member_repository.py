import sqlite3
from typing import Optional, List
from src.domain.entities.member import Member
from src.domain.enums.member_enums import MemberRole, MemberStatus
from src.domain.exceptions.member_exceptions import DuplicatePhoneException, MemberNotFoundException
from src.domain.ports.member_repository import MemberRepository


class SqliteMemberRepository(MemberRepository):
    """Adaptador de persistência SQLite implementando a porta MemberRepository."""

    def __init__(self, connection: sqlite3.Connection):
        self.conn = connection

    def create(self, member: Member) -> Member:
        try:
            with self.conn:
                self.conn.execute(
                    """
                    INSERT INTO members (id, name, phone, email, role, status, created_at, updated_at)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                    """,
                    (
                        member.id,
                        member.name,
                        member.phone,
                        member.email,
                        member.role.value,
                        member.status.value,
                        member.created_at.isoformat(),
                        member.updated_at.isoformat(),
                    ),
                )
            return member
        except sqlite3.IntegrityError as e:
            if "UNIQUE constraint failed" in str(e) or "idx_members_active_phone" in str(e):
                raise DuplicatePhoneException(phone=member.phone)
            raise

    def find_active_by_phone(self, phone: str) -> Optional[Member]:
        cursor = self.conn.execute(
            """
            SELECT id, name, phone, email, role, status, created_at, updated_at
            FROM members
            WHERE phone = ? AND status = 'active'
            LIMIT 1
            """,
            (phone,),
        )
        row = cursor.fetchone()
        if not row:
            return None
        return Member.reconstitute(
            id=row["id"],
            name=row["name"],
            phone=row["phone"],
            email=row["email"],
            role=row["role"],
            status=row["status"],
            created_at=row["created_at"],
            updated_at=row["updated_at"],
        )

    def find_by_id(self, member_id: str) -> Optional[Member]:
        cursor = self.conn.execute(
            """
            SELECT id, name, phone, email, role, status, created_at, updated_at
            FROM members
            WHERE id = ?
            LIMIT 1
            """,
            (member_id,),
        )
        row = cursor.fetchone()
        if not row:
            return None
        return Member.reconstitute(
            id=row["id"],
            name=row["name"],
            phone=row["phone"],
            email=row["email"],
            role=row["role"],
            status=row["status"],
            created_at=row["created_at"],
            updated_at=row["updated_at"],
        )

    def find_all(
        self,
        status: Optional[MemberStatus] = None,
        role: Optional[MemberRole] = None,
        search: Optional[str] = None,
    ) -> List[Member]:
        query = "SELECT id, name, phone, email, role, status, created_at, updated_at FROM members WHERE 1=1"
        params = []

        if status:
            query += " AND status = ?"
            params.append(status.value)

        if role:
            query += " AND role = ?"
            params.append(role.value)

        if search:
            query += " AND name LIKE ? COLLATE NOCASE"
            params.append(f"%{search.strip()}%")

        query += " ORDER BY name COLLATE NOCASE ASC"

        cursor = self.conn.execute(query, params)
        rows = cursor.fetchall()
        return [
            Member.reconstitute(
                id=r["id"],
                name=r["name"],
                phone=r["phone"],
                email=r["email"],
                role=r["role"],
                status=r["status"],
                created_at=r["created_at"],
                updated_at=r["updated_at"],
            )
            for r in rows
        ]

    def update(self, member: Member) -> Member:
        try:
            with self.conn:
                cursor = self.conn.execute(
                    """
                    UPDATE members
                    SET name = ?, phone = ?, email = ?, role = ?, status = ?, updated_at = ?
                    WHERE id = ?
                    """,
                    (
                        member.name,
                        member.phone,
                        member.email,
                        member.role.value,
                        member.status.value,
                        member.updated_at.isoformat(),
                        member.id,
                    ),
                )
                if cursor.rowcount == 0:
                    raise MemberNotFoundException(member_id=member.id)
            return member
        except sqlite3.IntegrityError as e:
            if "UNIQUE constraint failed" in str(e) or "idx_members_active_phone" in str(e):
                raise DuplicatePhoneException(phone=member.phone)
            raise
