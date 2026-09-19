from fastapi import APIRouter, Depends, Request
from fastapi.responses import HTMLResponse
from sqlalchemy import select
from sqlalchemy.orm import Session
import jdatetime

from ..config import APP_NAME
from ..database import get_db
from ..models import (
    Category,
    Poster,
    Prize,
    ParticipantGroup,
    SocialLink,
    Winner,
    Submission,
)


router = APIRouter()


def jalali_now_text() -> str:
    """
    Return today's Jalali date as YYYY/MM/DD.
    """
    now = jdatetime.datetime.now()
    return now.strftime("%Y/%m/%d")


def common_context(db: Session, request: Request) -> dict:
    """
    Common data used by public templates.
    """

    return {
        "request": request,
        "app_name": APP_NAME,

        "categories": db.scalars(
            select(Category)
            .order_by(Category.id)
        ).all(),

        "posters": db.scalars(
            select(Poster)
            .where(Poster.active.is_(True))
            .order_by(Poster.id.desc())
        ).all(),

        "prizes": db.scalars(
            select(Prize)
            .order_by(Prize.sort_order, Prize.id)
        ).all(),

        "participant_groups": db.scalars(
            select(ParticipantGroup)
            .order_by(ParticipantGroup.id)
        ).all(),

        "social_links": db.scalars(
            select(SocialLink)
            .order_by(SocialLink.id)
        ).all(),

        "winners": db.scalars(
            select(Winner)
            .where(Winner.published.is_(True))
            .order_by(Winner.id.desc())
        ).all(),

        "jalali_today": jalali_now_text(),
    }


@router.get("/", response_class=HTMLResponse)
def home(
    request: Request,
    db: Session = Depends(get_db),
):
    context = common_context(db, request)

    return request.app.state.templates.TemplateResponse(
        request=request,
        name="index.html",
        context=context,
    )


@router.get("/festival", response_class=HTMLResponse)
def festival(
    request: Request,
    db: Session = Depends(get_db),
):
    context = common_context(db, request)

    return request.app.state.templates.TemplateResponse(
        request=request,
        name="festival.html",
        context=context,
    )


@router.get("/rules", response_class=HTMLResponse)
def rules(
    request: Request,
    db: Session = Depends(get_db),
):
    context = common_context(db, request)

    return request.app.state.templates.TemplateResponse(
        request=request,
        name="rules.html",
        context=context,
    )


@router.get("/winners", response_class=HTMLResponse)
def winners(
    request: Request,
    db: Session = Depends(get_db),
):
    context = common_context(db, request)

    return request.app.state.templates.TemplateResponse(
        request=request,
        name="winners.html",
        context=context,
    )


@router.get("/participants", response_class=HTMLResponse)
def participants(
    request: Request,
    db: Session = Depends(get_db),
):
    context = common_context(db, request)

    return request.app.state.templates.TemplateResponse(
        request=request,
        name="participants.html",
        context=context,
    )


@router.get("/submit", response_class=HTMLResponse)
def submit_page(
    request: Request,
    db: Session = Depends(get_db),
):
    context = common_context(db, request)

    return request.app.state.templates.TemplateResponse(
        request=request,
        name="submit.html",
        context=context,
    )


@router.get("/api/stats")
def stats(
    db: Session = Depends(get_db),
):
    return {
        "submissions": db.query(Submission).count(),
        "categories": db.query(Category).count(),
        "winners": db.query(Winner)
        .filter(Winner.published.is_(True))
        .count(),
    }

