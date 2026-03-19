from http import HTTPStatus

from flask import g, redirect

from app.blueprints.redirect import redirect_bp
from app.blueprints.redirect.repository import RedirectRepository
from app.blueprints.redirect.service import RedirectService


def get_service() -> RedirectService:
    if "redirect_service" not in g:
        g.redirect_service = RedirectService(RedirectRepository())
    return g.redirect_service


@redirect_bp.get("/<string:short_code>")
@redirect_bp.response(HTTPStatus.FOUND)
def resolve(short_code: str):
    url = get_service().resolve_short_code(short_code)
    return redirect(url.original_url, code=HTTPStatus.FOUND.value)
