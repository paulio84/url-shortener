from http import HTTPStatus

from flask import g
from flask_jwt_extended import (
    create_access_token,
    create_refresh_token,
    get_jwt_identity,
    jwt_required,
)

from app.blueprints.auth import auth_bp
from app.blueprints.auth.repository import AuthRepository
from app.blueprints.auth.service import AuthService
from app.extensions import limiter
from app.schemas.user import (
    LoginRequestSchema,
    LoginResponseSchema,
    RefreshResponseSchema,
    RegisterRequestSchema,
    UserResponseSchema,
)


def get_service() -> AuthService:
    if "auth_service" not in g:
        g.auth_service = AuthService(AuthRepository())
    return g.auth_service


@auth_bp.post("/register")
@limiter.limit("3 per minute")
@auth_bp.response(HTTPStatus.CREATED, UserResponseSchema)
@auth_bp.arguments(RegisterRequestSchema)
def register(request_data: RegisterRequestSchema):
    return get_service().register(request_data["email"], request_data["password"])


@auth_bp.post("/login")
@limiter.limit("5 per minute")
@auth_bp.response(HTTPStatus.OK, LoginResponseSchema)
@auth_bp.arguments(LoginRequestSchema)
def login(request_data: LoginRequestSchema):
    user = get_service().login(request_data["email"], request_data["password"])

    access_token = create_access_token(identity=str(user.id))
    refresh_token = create_refresh_token(identity=str(user.id))

    return {
        "access_token": access_token,
        "refresh_token": refresh_token,
        "user": user,
    }


@auth_bp.post("/refresh")
@jwt_required(refresh=True)
@auth_bp.doc(security=[{"bearerAuth": []}])
@auth_bp.response(HTTPStatus.OK, RefreshResponseSchema)
def refresh():
    identity = get_jwt_identity()
    access_token = create_access_token(identity=identity)
    return {"access_token": access_token}
