from http import HTTPStatus

from flask import g, jsonify, request
from marshmallow import ValidationError as MarshmallowValidationError

from app.blueprints.urls import urls_bp
from app.blueprints.urls.repository import URLRepository
from app.blueprints.urls.service import URLService
from app.errors import ValidationError
from app.schemas.url import (
    shorten_request_schema,
    url_response_list_schema,
    url_response_schema,
)


def get_service() -> URLService:
    if "url_service" not in g:
        g.url_service = URLService(URLRepository())
    return g.url_service


@urls_bp.post("/shorten")
def shorten_url():
    try:
        data = shorten_request_schema.load(request.get_json(silent=True) or {})
    except MarshmallowValidationError as e:
        raise ValidationError(str(e.messages))

    url = get_service().create_short_url(data["url"])
    return jsonify(url_response_schema.dump(url)), HTTPStatus.CREATED.value


@urls_bp.get("/urls")
def list_urls():
    urls = get_service().get_all()
    return jsonify(url_response_list_schema.dump(urls)), HTTPStatus.OK.value


@urls_bp.get("/urls/<string:short_code>")
def get_url(short_code: str):
    url = get_service().get_by_short_code(short_code)
    return jsonify(url_response_schema.dump(url)), HTTPStatus.OK.value
