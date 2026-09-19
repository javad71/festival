from fastapi import APIRouter, Depends, File, Form, Request, UploadFile, HTTPException
from fastapi.responses import HTMLResponse, RedirectResponse
from sqlalchemy import func, or_, select
from sqlalchemy.orm import Session
import secrets
from ..auth import require_admin, verify_credentials
from ..database import get_db
from ..models import Submission, Category, Winner
from ..services.uploads import save_image_upload

router = APIRouter(prefix="/admin")

def csrf_token(request: Request) -> str:
    token = request.session.get("csrf_token")
    if not token:
        token = secrets.token_urlsafe(32)
        request.session["csrf_token"] = token
    return token

def verify_csrf(request: Request, token: str):
    expected = request.session.get("csrf_token")
    if not expected or not secrets.compare_digest(expected, token):
        raise HTTPException(status_code=403, detail="درخواست نامعتبر است.")

@router.get("/login", response_class=HTMLResponse)
def login_page(request: Request):
    if request.session.get("admin_authenticated"):
        return RedirectResponse("/admin", status_code=303)
    return request.app.state.templates.TemplateResponse(request=request, name="admin_login.html", context={"request": request, "error": None, "csrf_token": csrf_token(request)})

@router.post("/login")
def login(request: Request, username: str = Form(...), password: str = Form(...), csrf: str = Form(...)):
    verify_csrf(request, csrf)
    if not verify_credentials(username.strip(), password):
        return request.app.state.templates.TemplateResponse(request=request, name="admin_login.html", context={"request": request, "error": "نام کاربری یا رمز عبور صحیح نیست.", "csrf_token": csrf_token(request)}, status_code=401)
    request.session.clear()
    request.session["admin_authenticated"] = True
    request.session["admin_username"] = username.strip()
    csrf_token(request)
    return RedirectResponse("/admin", status_code=303)

@router.post("/logout")
def logout(request: Request):
    request.session.clear()
    return RedirectResponse("/admin/login", status_code=303)

@router.get("", response_class=HTMLResponse, dependencies=[Depends(require_admin)])
def dashboard(request: Request, db: Session = Depends(get_db), q: str = "", status: str = "all", category: str = "all"):
    stmt = select(Submission).order_by(Submission.id.desc())
    if q.strip():
        term = f"%{q.strip()}%"
        stmt = stmt.where(or_(Submission.full_name.ilike(term), Submission.phone.ilike(term), Submission.title.ilike(term), Submission.original_filename.ilike(term)))
    if status in {"pending", "approved", "rejected"}:
        stmt = stmt.where(Submission.status == status)
    if category != "all":
        stmt = stmt.where(Submission.category_slug == category)
    submissions = db.scalars(stmt).all()
    categories = db.scalars(select(Category).order_by(Category.id)).all()
    winners = db.scalars(select(Winner).order_by(Winner.id.desc())).all()
    # Only approved submissions are offered as winner candidates. A submission can
    # be selected once; its existing uploaded file is reused automatically.
    used_submission_ids = set(db.scalars(select(Winner.source_submission_id).where(Winner.source_submission_id.is_not(None))).all())
    winner_candidates = db.scalars(
        select(Submission)
        .where(Submission.status == "approved", ~Submission.id.in_(used_submission_ids) if used_submission_ids else True)
        .order_by(Submission.id.desc())
    ).all()
    stats = {
        "total": db.query(Submission).count(),
        "pending": db.query(Submission).filter(Submission.status == "pending").count(),
        "approved": db.query(Submission).filter(Submission.status == "approved").count(),
        "rejected": db.query(Submission).filter(Submission.status == "rejected").count(),
        "winners": db.query(Winner).count(),
    }
    context = {"request": request, "submissions": submissions, "categories": categories, "winners": winners, "winner_candidates": winner_candidates, "stats": stats, "q": q, "status": status, "category": category, "csrf_token": csrf_token(request)}
    return request.app.state.templates.TemplateResponse(request=request, name="admin.html", context=context)

@router.post("/submissions/{submission_id}/status", dependencies=[Depends(require_admin)])
def update_status(request: Request, submission_id: int, status: str = Form(...), csrf: str = Form(...), db: Session = Depends(get_db)):
    verify_csrf(request, csrf)
    if status not in {"pending", "approved", "rejected"}: status = "pending"
    submission = db.get(Submission, submission_id)
    if submission:
        submission.status = status
        db.commit()
    return RedirectResponse(url="/admin", status_code=303)

@router.post("/winners/create", dependencies=[Depends(require_admin)])
def create_winner(
    request: Request,
    csrf: str = Form(...),
    submission_id: int = Form(...),
    rank_title: str = Form(...),
    description: str = Form(""),
    db: Session = Depends(get_db),
):
    verify_csrf(request, csrf)
    submission = db.get(Submission, submission_id)
    if not submission or submission.status != "approved":
        raise HTTPException(status_code=400, detail="اثر انتخاب‌شده باید تأیید شده باشد.")

    existing = db.scalar(select(Winner).where(Winner.source_submission_id == submission.id))
    if existing:
        raise HTTPException(status_code=409, detail="این اثر قبلاً به عنوان برگزیده ثبت شده است.")

    winner = Winner(
        source_submission_id=submission.id,
        full_name=submission.full_name.strip(),
        category_slug=submission.category_slug,
        rank_title=rank_title.strip(),
        work_title=submission.title.strip(),
        description=(description.strip() or (submission.description or "").strip()),
        # Reuse the exact file already uploaded by the participant. No second upload.
        image_path=submission.file_path,
        published=True,
    )
    db.add(winner)
    db.commit()
    return RedirectResponse("/admin", status_code=303)

@router.post("/winners/{winner_id}/edit", dependencies=[Depends(require_admin)])
async def edit_winner(
    request: Request, winner_id: int, csrf: str = Form(...), full_name: str = Form(...), category_slug: str = Form(...),
    rank_title: str = Form(...), work_title: str = Form(...), description: str = Form(""), image: UploadFile | None = File(None), db: Session = Depends(get_db)
):
    verify_csrf(request, csrf)
    winner = db.get(Winner, winner_id)
    if winner:
        winner.full_name = full_name.strip()
        winner.category_slug = category_slug
        winner.rank_title = rank_title.strip()
        winner.work_title = work_title.strip()
        winner.description = description.strip()
        if image and image.filename:
            winner.image_path, _ = await save_image_upload(image)
        db.commit()
    return RedirectResponse("/admin", status_code=303)

@router.post("/winners/{winner_id}/toggle", dependencies=[Depends(require_admin)])
def toggle_winner(request: Request, winner_id: int, csrf: str = Form(...), db: Session = Depends(get_db)):
    verify_csrf(request, csrf)
    winner = db.get(Winner, winner_id)
    if winner:
        winner.published = not winner.published
        db.commit()
    return RedirectResponse("/admin", status_code=303)

@router.post("/winners/{winner_id}/delete", dependencies=[Depends(require_admin)])
def delete_winner(request: Request, winner_id: int, csrf: str = Form(...), db: Session = Depends(get_db)):
    verify_csrf(request, csrf)
    winner = db.get(Winner, winner_id)
    if winner:
        db.delete(winner); db.commit()
    return RedirectResponse("/admin", status_code=303)
