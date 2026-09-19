from pathlib import Path
from uuid import uuid4
from fastapi import UploadFile, HTTPException
from ..config import UPLOAD_DIR, MAX_UPLOAD_MB, ALLOWED_EXTENSIONS

async def save_upload(file: UploadFile) -> tuple[str, str]:
    if not file.filename:
        raise HTTPException(400, "فایلی انتخاب نشده است.")

    ext = Path(file.filename).suffix.lower()
    media_type = None
    for kind, extensions in ALLOWED_EXTENSIONS.items():
        if ext in extensions:
            media_type = kind
            break

    if not media_type:
        raise HTTPException(400, "فرمت فایل مجاز نیست.")

    content = await file.read()
    max_bytes = MAX_UPLOAD_MB * 1024 * 1024
    if len(content) > max_bytes:
        raise HTTPException(413, f"حجم فایل نباید بیشتر از {MAX_UPLOAD_MB} مگابایت باشد.")

    folder = UPLOAD_DIR / media_type
    folder.mkdir(parents=True, exist_ok=True)

    safe_name = f"{uuid4().hex}{ext}"
    destination = folder / safe_name
    destination.write_bytes(content)

    relative = f"/uploads/{media_type}/{safe_name}"
    return relative, file.filename
