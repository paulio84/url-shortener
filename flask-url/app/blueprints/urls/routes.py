from http import HTTPStatus

from flask import g, jsonify, request
from flask_jwt_extended import get_jwt_identity, jwt_required
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
@jwt_required()
def shorten_url():
    try:
        data = shorten_request_schema.load(request.get_json(silent=True) or {})
    except MarshmallowValidationError as e:
        raise ValidationError(str(e.messages))

    user_id = int(get_jwt_identity())
    url = get_service().create_short_url(data["url"], user_id)
    return jsonify(url_response_schema.dump(url)), HTTPStatus.CREATED.value


@urls_bp.get("/urls")
@jwt_required()
def list_urls():
    user_id = int(get_jwt_identity())
    urls = get_service().get_all_for_user(user_id)
    return jsonify(url_response_list_schema.dump(urls)), HTTPStatus.OK.value


@urls_bp.get("/urls/<string:short_code>")
@jwt_required()
def get_url(short_code: str):
    user_id = int(get_jwt_identity())
    url = get_service().get_by_short_code_for_user(short_code, user_id)
    return jsonify(url_response_schema.dump(url)), HTTPStatus.OK.value
