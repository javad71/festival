from pathlib import Path
from uuid import uuid4
from fastapi import UploadFile, HTTPException
from ..config import UPLOAD_DIR, MAX_UPLOAD_MB, ALLOWED_EXTENSIONS, IMAGE_EXTENSIONS

async def save_upload(file: UploadFile, allowed_kinds=None) -> tuple[str, str]:
    if not file.filename:
        raise HTTPException(400, "فایلی انتخاب نشده است.")

    ext = Path(file.filename).suffix.lower()
    media_type = next((kind for kind, extensions in ALLOWED_EXTENSIONS.items() if ext in extensions), None)
    if not media_type or (allowed_kinds and media_type not in allowed_kinds):
        raise HTTPException(400, "فرمت فایل مجاز نیست.")

    content = await file.read()
    if len(content) > MAX_UPLOAD_MB * 1024 * 1024:
        raise HTTPException(413, f"حجم فایل نباید بیشتر از {MAX_UPLOAD_MB} مگابایت باشد.")

    folder = UPLOAD_DIR / media_type
    folder.mkdir(parents=True, exist_ok=True)
    safe_name = f"{uuid4().hex}{ext}"
    (folder / safe_name).write_bytes(content)
    return f"/uploads/{media_type}/{safe_name}", file.filename

async def save_image_upload(file: UploadFile) -> tuple[str, str]:
    return await save_upload(file, allowed_kinds={"image"})
