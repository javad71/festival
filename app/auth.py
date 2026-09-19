import base64
import hashlib
import hmac
import os
from fastapi import Depends, HTTPException, Request
from fastapi.responses import RedirectResponse
from .config import ADMIN_USERNAME, ADMIN_PASSWORD, ADMIN_PASSWORD_HASH


def _verify_password(password: str) -> bool:
    if ADMIN_PASSWORD_HASH:
        try:
            raw = base64.b64decode(ADMIN_PASSWORD_HASH.encode())
            salt, expected = raw[:16], raw[16:]
            actual = hashlib.pbkdf2_hmac("sha256", password.encode(), salt, 210_000)
            return hmac.compare_digest(actual, expected)
        except Exception:
            return False
    return hmac.compare_digest(password, ADMIN_PASSWORD)


def verify_credentials(username: str, password: str) -> bool:
    return hmac.compare_digest(username, ADMIN_USERNAME) and _verify_password(password)


def require_admin(request: Request):
    if not request.session.get("admin_authenticated"):
        raise HTTPException(status_code=303, headers={"Location": "/admin/login"})
    return True


def redirect_if_admin(request: Request):
    if request.session.get("admin_authenticated"):
        return RedirectResponse("/admin", status_code=303)
    return None
