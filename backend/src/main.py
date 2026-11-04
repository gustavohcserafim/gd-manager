import os
from typing import Optional
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from src.infrastructure.database.connection import get_connection, init_db
from src.infrastructure.database.sqlite_member_repository import SqliteMemberRepository
from src.infrastructure.web.routers.members_router import router as members_router, get_repository


def create_app(repo: Optional[SqliteMemberRepository] = None, db_path: Optional[str] = None) -> FastAPI:
    app = FastAPI(
        title="GD Manager API",
        version="1.0.0",
        description="API REST para gestão de membros do GD Manager em Clean Architecture.",
    )

    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    if repo is None:
        target_db = db_path if db_path is not None else os.getenv("DATABASE_PATH", "gd_manager.db")
        conn = get_connection(db_path=target_db)
        init_db(conn=conn)
        repo = SqliteMemberRepository(conn)

    app.dependency_overrides[get_repository] = lambda: repo
    app.include_router(members_router)

    return app


app = create_app()
