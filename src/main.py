from contextlib import asynccontextmanager
from pathlib import Path
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from src.services.database import get_db_connection, init_db
from src.services.seed import seed_initial_leaders
from src.api.routes_auth import router as auth_router
from src.api.routes_members import router as members_router
from src.api.routes_history import router as history_router



@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup: Ensure database tables and initial seed data exist
    conn = get_db_connection()
    try:
        init_db(conn)
        seed_initial_leaders(conn)
    finally:
        conn.close()
    yield
    # Shutdown

app = FastAPI(
    title="GD Manager",
    description="Sistema de Gestão do GD - Igreja Onda Mooca",
    version="1.0.0",
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth_router)
app.include_router(members_router)
app.include_router(history_router)




# Static directory setup
static_dir = Path(__file__).parent / "static"
if not static_dir.exists():
    try:
        static_dir.mkdir(parents=True, exist_ok=True)
    except Exception:
        pass

if static_dir.exists():
    app.mount("/static", StaticFiles(directory=str(static_dir)), name="static")


@app.get("/")
def serve_index():
    index_file = static_dir / "index.html"
    if index_file.exists():
        return FileResponse(index_file)
    return {"message": "GD Manager API is running"}


@app.get("/sw.js")
def serve_sw():
    sw_file = static_dir / "sw.js"
    if sw_file.exists():
        return FileResponse(sw_file, media_type="application/javascript", headers={"Service-Worker-Allowed": "/"})
    return {"error": "Not found"}


@app.get("/manifest.json")
def serve_manifest():
    manifest_file = static_dir / "manifest.json"
    if manifest_file.exists():
        return FileResponse(manifest_file, media_type="application/manifest+json")
    return {"error": "Not found"}


@app.get("/health")
def health_check():
    return {"status": "ok", "app": "GD Manager"}
