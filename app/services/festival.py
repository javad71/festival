from datetime import datetime, timezone
from .uploads import *  # noqa: F401,F403
from ..config import FESTIVAL_START_DATE, FESTIVAL_END_DATE


def _date(value: str):
    return datetime.fromisoformat(value).replace(tzinfo=timezone.utc)


def festival_phase(now=None) -> str:
    now = now or datetime.now(timezone.utc)
    start = _date(FESTIVAL_START_DATE)
    end = _date(FESTIVAL_END_DATE)
    if now < start:
        return "countdown"
    if now < end:
        return "festival"
    return "winners"


def festival_context():
    phase = festival_phase()
    return {
        "festival_phase": phase,
        "festival_start": FESTIVAL_START_DATE,
        "festival_end": FESTIVAL_END_DATE,
    }
