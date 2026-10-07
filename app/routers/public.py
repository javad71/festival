from fastapi import APIRouter, Depends, Request
from fastapi.responses import HTMLResponse
from sqlalchemy import select, func
from sqlalchemy.orm import Session
import jdatetime
from ..config import APP_NAME, WINNERS_VISIBLE_BEFORE_END
from ..database import get_db
from ..models import Category, Poster, Prize, ParticipantGroup, SocialLink, Winner, Submission
from ..services.festival import festival_context

router = APIRouter()

def jalali_now_text():
    return jdatetime.datetime.now().strftime("%Y/%m/%d")

def common_context(db: Session, request: Request) -> dict:
    context = {
        "request": request, "app_name": APP_NAME,
        "categories": db.scalars(select(Category).order_by(Category.id)).all(),
        "posters": db.scalars(select(Poster).where(Poster.active.is_(True)).order_by(Poster.id.desc())).all(),
        "prizes": db.scalars(select(Prize).order_by(Prize.sort_order, Prize.id)).all(),
        "participant_groups": db.scalars(select(ParticipantGroup).order_by(ParticipantGroup.id)).all(),
        "social_links": db.scalars(select(SocialLink).order_by(SocialLink.id)).all(),
        "jalali_today": jalali_now_text(),
    }
    context.update(festival_context())

    # Public, aggregate-only festival momentum statistics.
    total_submissions = db.query(Submission).count()
    approved_submissions = db.query(Submission).filter(Submission.status == "approved").count()
    pending_submissions = db.query(Submission).filter(Submission.status == "pending").count()
    unique_participants = (
        db.query(func.count(func.distinct(Submission.phone)))
        .scalar()
        or 0
    )
    category_counts = dict(
        db.query(Submission.category_slug, func.count(Submission.id))
        .group_by(Submission.category_slug)
        .all()
    )
    category_stats = []
    for category in context["categories"]:
        category_stats.append({
            "slug": category.slug,
            "title": category.title,
            "icon": category.icon,
            "count": int(category_counts.get(category.slug, 0)),
        })

    context["festival_stats"] = {
        "submissions": total_submissions,
        "approved": approved_submissions,
        "pending": pending_submissions,
        "participants": unique_participants,
        "categories": len(context["categories"]),
        "category_stats": category_stats,
        "approval_rate": round((approved_submissions / total_submissions) * 100) if total_submissions else 0,
    }

    winners = db.scalars(select(Winner).where(Winner.published.is_(True)).order_by(Winner.id.desc())).all()
    if context["festival_phase"] == "winners" or WINNERS_VISIBLE_BEFORE_END:
        context["winners"] = winners
    else:
        context["winners"] = []
    context["winners_visible_before_end"] = WINNERS_VISIBLE_BEFORE_END
    return context

@router.get("/", response_class=HTMLResponse)
def home(request: Request, db: Session = Depends(get_db)):
    return request.app.state.templates.TemplateResponse(request=request, name="index.html", context=common_context(db, request))

@router.get("/festival", response_class=HTMLResponse)
def festival(request: Request, db: Session = Depends(get_db)):
    return request.app.state.templates.TemplateResponse(request=request, name="festival.html", context=common_context(db, request))

@router.get("/rules", response_class=HTMLResponse)
def rules(request: Request, db: Session = Depends(get_db)):
    return request.app.state.templates.TemplateResponse(request=request, name="rules.html", context=common_context(db, request))

@router.get("/winners", response_class=HTMLResponse)
def winners(request: Request, db: Session = Depends(get_db)):
    return request.app.state.templates.TemplateResponse(request=request, name="winners.html", context=common_context(db, request))

@router.get("/participants", response_class=HTMLResponse)
def participants(request: Request, db: Session = Depends(get_db)):
    return request.app.state.templates.TemplateResponse(request=request, name="participants.html", context=common_context(db, request))

@router.get("/submit", response_class=HTMLResponse)
def submit_page(request: Request, db: Session = Depends(get_db)):
    return request.app.state.templates.TemplateResponse(request=request, name="submit.html", context=common_context(db, request))

@router.get("/api/stats")
def stats(db: Session = Depends(get_db)):
    total = db.query(Submission).count()
    approved = db.query(Submission).filter(Submission.status == "approved").count()
    category_counts = dict(
        db.query(Submission.category_slug, func.count(Submission.id))
        .group_by(Submission.category_slug)
        .all()
    )
    return {
        "submissions": total,
        "approved": approved,
        "pending": db.query(Submission).filter(Submission.status == "pending").count(),
        "rejected": db.query(Submission).filter(Submission.status == "rejected").count(),
        "participants": db.query(func.count(func.distinct(Submission.phone))).scalar() or 0,
        "categories": db.query(Category).count(),
        "winners": db.query(Winner).filter(Winner.published.is_(True)).count(),
        "approval_rate": round((approved / total) * 100) if total else 0,
        "category_counts": category_counts,
    }
