from fastapi import APIRouter, Depends, Form, Request
from fastapi.responses import HTMLResponse, RedirectResponse
from sqlalchemy import select
from sqlalchemy.orm import Session

from ..database import get_db
from ..models import Submission, Category, Winner


router = APIRouter(prefix="/admin")


@router.get("", response_class=HTMLResponse)
def dashboard(
    request: Request,
    db: Session = Depends(get_db),
):
    submissions = db.scalars(
        select(Submission)
        .order_by(Submission.id.desc())
    ).all()

    categories = db.scalars(
        select(Category)
        .order_by(Category.id)
    ).all()

    winners = db.scalars(
        select(Winner)
        .order_by(Winner.id.desc())
    ).all()

    context = {
        "request": request,
        "submissions": submissions,
        "categories": categories,
        "winners": winners,
    }

    return request.app.state.templates.TemplateResponse(
        request=request,
        name="admin.html",
        context=context,
    )


@router.post("/submissions/{submission_id}/status")
def update_status(
    submission_id: int,
    status: str = Form(...),
    db: Session = Depends(get_db),
):
    allowed_statuses = {
        "pending",
        "approved",
        "rejected",
    }

    if status not in allowed_statuses:
        status = "pending"

    submission = db.get(
        Submission,
        submission_id,
    )

    if submission:
        submission.status = status
        db.commit()

    return RedirectResponse(
        url="/admin",
        status_code=303,
    )