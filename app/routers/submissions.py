from fastapi import APIRouter, Depends, File, Form, HTTPException, UploadFile
from sqlalchemy import select
from sqlalchemy.orm import Session
from ..database import get_db
from ..models import Submission, Category
from ..services.uploads import save_upload
from ..services.festival import festival_phase

router = APIRouter(prefix="/api/submissions", tags=["submissions"])

@router.post("")
async def create_submission(
    full_name: str = Form(...),
    phone: str = Form(...),
    email: str = Form(""),
    city: str = Form(""),
    age_group: str = Form(""),
    category_slug: str = Form(...),
    title: str = Form(...),
    description: str = Form(""),
    rules_accepted: str = Form(...),
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
):
    if festival_phase() == "winners":
        raise HTTPException(400, "مهلت ارسال آثار به پایان رسیده است.")

    if rules_accepted.lower() not in {"true", "1", "on", "yes"}:
        raise HTTPException(400, "پذیرش قوانین جشنواره الزامی است.")

    category = db.scalar(select(Category).where(Category.slug == category_slug))
    if not category:
        raise HTTPException(400, "محور انتخاب‌شده معتبر نیست.")

    file_path, original_name = await save_upload(file)

    submission = Submission(
        full_name=full_name.strip(),
        phone=phone.strip(),
        email=email.strip() or None,
        city=city.strip() or None,
        age_group=age_group.strip() or None,
        category_slug=category_slug,
        title=title.strip(),
        description=description.strip() or None,
        file_path=file_path,
        original_filename=original_name,
    )
    db.add(submission)
    db.commit()
    db.refresh(submission)

    return {
        "success": True,
        "message": "اثر شما با موفقیت ثبت شد. پس از بررسی، وضعیت اثر در سامانه به‌روزرسانی می‌شود.",
        "submission_id": submission.id,
    }
