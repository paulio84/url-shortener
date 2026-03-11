from http import HTTPStatus

from flask import g, jsonify, request
from flask_jwt_extended import (
    create_access_token,
    create_refresh_token,
    get_jwt_identity,
    jwt_required,
)
from marshmallow import ValidationError as MarshmallowValidationError

from app.blueprints.auth import auth_bp
from app.blueprints.auth.repository import AuthRepository
from app.blueprints.auth.service import AuthService
from app.errors import ValidationError
from app.schemas.user import (
    login_request_schema,
    register_request_schema,
    user_response_schema,
)


def get_service() -> AuthService:
    if "auth_service" not in g:
        g.auth_service = AuthService(AuthRepository())
    return g.auth_service


@auth_bp.post("/register")
def register():
    try:
        data = register_request_schema.load(request.get_json(silent=True) or {})
    except MarshmallowValidationError as e:
        raise ValidationError(str(e.messages))

    user = get_service().register(data["email"], data["password"])
    return jsonify(user_response_schema.dump(user)), HTTPStatus.CREATED.value


@auth_bp.post("/login")
def login():
    try:
        data = login_request_schema.load(request.get_json(silent=True) or {})
    except MarshmallowValidationError as e:
        raise ValidationError(str(e.messages))

    user = get_service().login(data["email"], data["password"])

    access_token = create_access_token(identity=str(user.id))
    refresh_token = create_refresh_token(identity=str(user.id))

    return jsonify(
        {
            "access_token": access_token,
            "refresh_token": refresh_token,
            "user": user_response_schema.dump(user),
        }
    ), HTTPStatus.OK.value


@auth_bp.post("/refresh")
@jwt_required(refresh=True)
def refresh():
    identity = get_jwt_identity()
    access_token = create_access_token(identity=identity)
    return jsonify({"access_token", access_token}), HTTPStatus.OK.value
