from pathlib import Path
import os
from dotenv import load_dotenv


# ---------------------------------------------------------
# Project paths
# ---------------------------------------------------------
BASE_DIR = Path(__file__).resolve().parent.parent

# Load .env from the project root
ENV_FILE = BASE_DIR / ".env"
load_dotenv(dotenv_path=ENV_FILE)


# ---------------------------------------------------------
# Application configuration
# ---------------------------------------------------------
APP_NAME = os.getenv(
    "APP_NAME",
    "جشنواره نفس‌های آینده",
)

SECRET_KEY = os.getenv(
    "SECRET_KEY",
    "development-secret-change-me",
)

DATABASE_URL = os.getenv(
    "DATABASE_URL",
    f"sqlite:///{BASE_DIR / 'festival.db'}",
)

MAX_UPLOAD_MB = int(
    os.getenv(
        "MAX_UPLOAD_MB",
        "50",
    )
)

# ---------------------------------------------------------
# Upload configuration
# ---------------------------------------------------------
UPLOAD_DIR = BASE_DIR / os.getenv(
    "UPLOAD_DIR",
    "uploads",
)

UPLOAD_DIR.mkdir(
    parents=True,
    exist_ok=True,
)


# ---------------------------------------------------------
# Allowed upload extensions
# ---------------------------------------------------------
ALLOWED_EXTENSIONS = {
    "image": {
        ".jpg",
        ".jpeg",
        ".png",
        ".webp",
    },
    "video": {
        ".mp4",
        ".mov",
        ".webm",
    },
    "document": {
        ".pdf",
    },
}


