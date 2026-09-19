# جشنواره نفس‌های آینده

A complete RTL Persian festival website built with FastAPI, Jinja2, SQLAlchemy, vanilla JavaScript and CSS.

## Features

- RTL Persian responsive UI
- Light / dark mode
- Jalali countdown to 1405/10/01
- Festival categories
- Poster gallery
- Festival rules
- Prizes
- Eligible participants
- Online submission/upload
- Submission database
- Winners section
- Social media links
- Simple admin dashboard
- SQLite by default
- Modular FastAPI architecture
- File validation and safe generated filenames

## Run

### Windows

```powershell
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
uvicorn app.main:app --reload
```

### Linux/macOS

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload
```

Open:

http://127.0.0.1:8000

Admin:

http://127.0.0.1:8000/admin

## Configuration

Copy `.env.example` to `.env` and change `SECRET_KEY`.

For production, put the app behind HTTPS and add proper admin authentication before exposing `/admin`.
