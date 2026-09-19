from pathlib import Path
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from .config import APP_NAME, UPLOAD_DIR
from .database import Base, engine, SessionLocal
from .seed import seed_database
from .routers import public, submissions, admin

BASE_DIR = Path(__file__).resolve().parent.parent

app = FastAPI(
    title=APP_NAME,
    description="سامانه جشنواره نفس‌های آینده",
    version="1.0.0",
)

app.mount("/static", StaticFiles(directory=BASE_DIR / "static"), name="static")
app.mount("/uploads", StaticFiles(directory=UPLOAD_DIR), name="uploads")

app.state.templates = Jinja2Templates(directory=BASE_DIR / "templates")

Base.metadata.create_all(bind=engine)
with SessionLocal() as db:
    seed_database(db)

app.include_router(public.router)
app.include_router(submissions.router)
app.include_router(admin.router)
