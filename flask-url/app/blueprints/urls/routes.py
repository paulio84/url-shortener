from http import HTTPStatus

from flask import g
from flask_jwt_extended import jwt_required

from app.auth_utils import current_user_id
from app.blueprints.urls import urls_bp
from app.blueprints.urls.repository import URLRepository
from app.blueprints.urls.service import URLService
from app.schemas.url import (
    ShortenRequestSchema,
    URLResponseSchema,
)


def get_service() -> URLService:
    if "url_service" not in g:
        g.url_service = URLService(URLRepository())
    return g.url_service


@urls_bp.post("/shorten")
@jwt_required()
@urls_bp.response(HTTPStatus.CREATED, URLResponseSchema)
@urls_bp.arguments(ShortenRequestSchema)
def shorten_url(request_data: ShortenRequestSchema):
    return get_service().create_short_url(request_data["url"], current_user_id())


@urls_bp.get("/urls")
@jwt_required()
@urls_bp.response(HTTPStatus.OK, URLResponseSchema(many=True))
def list_urls():
    return get_service().get_all_for_user(current_user_id())


@urls_bp.get("/urls/<string:short_code>")
@jwt_required()
@urls_bp.response(HTTPStatus.OK, URLResponseSchema)
def get_url(short_code: str):
    return get_service().get_by_short_code_for_user(short_code, current_user_id())
