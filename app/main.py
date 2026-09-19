from pathlib import Path
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from starlette.middleware.sessions import SessionMiddleware
from .config import APP_NAME, UPLOAD_DIR, SECRET_KEY, SESSION_HTTPS_ONLY
from .database import Base, engine, SessionLocal
from sqlalchemy import inspect, text
from .seed import seed_database
from .routers import public, submissions, admin

BASE_DIR = Path(__file__).resolve().parent.parent

app = FastAPI(title=APP_NAME, description="سامانه جشنواره نفس‌های آینده", version="2.0.0")
app.add_middleware(
    SessionMiddleware,
    secret_key=SECRET_KEY,
    session_cookie="festival_admin_session",
    same_site="lax",
    https_only=SESSION_HTTPS_ONLY,
    max_age=60 * 60 * 12,
)
app.mount("/static", StaticFiles(directory=BASE_DIR / "static"), name="static")
app.mount("/uploads", StaticFiles(directory=UPLOAD_DIR), name="uploads")
app.state.templates = Jinja2Templates(directory=BASE_DIR / "templates")
Base.metadata.create_all(bind=engine)

# Lightweight schema migration for projects that already have festival.db.
def _ensure_winner_source_column():
    inspector = inspect(engine)
    columns = {column["name"] for column in inspector.get_columns("winners")}
    if "source_submission_id" not in columns:
        with engine.begin() as conn:
            conn.execute(text("ALTER TABLE winners ADD COLUMN source_submission_id INTEGER"))

_ensure_winner_source_column()

with SessionLocal() as db:
    seed_database(db)
app.include_router(public.router)
app.include_router(submissions.router)
app.include_router(admin.router)

@app.get("/health", tags=["system"])
def health():
    return {"status": "ok"}
