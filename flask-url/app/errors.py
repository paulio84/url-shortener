from http import HTTPStatus

from flask import Flask, jsonify
from werkzeug.exceptions import (
    BadRequest,
    HTTPException,
    TooManyRequests,
    UnprocessableEntity,
)


class APIError(Exception):
    """Base class for all API errors."""

    status_code = HTTPStatus.INTERNAL_SERVER_ERROR.value
    message = "An unexpected error occurred."

    def __init__(self, message: str | None = None, status_code: int | None = None):
        super().__init__(message or self.message)
        if message:
            self.message = message
        if status_code:
            self.status_code = status_code

    def to_dict(self) -> dict:
        return {
            "error": {
                "status": self.status_code,
                "message": self.message,
            }
        }


class NotFoundError(APIError):
    status_code = HTTPStatus.NOT_FOUND.value
    message = "Resource not found."


class ValidationError(APIError):
    status_code = HTTPStatus.UNPROCESSABLE_ENTITY.value
    message = "Invalid request data."


class ServiceError(APIError):
    status_code = HTTPStatus.INTERNAL_SERVER_ERROR.value
    message = "An internal service error occurred."


class MethodNotAllowedError(APIError):
    status_code = HTTPStatus.METHOD_NOT_ALLOWED.value
    message = "Method not allowed."


class UnauthorisedError(APIError):
    status_code = HTTPStatus.UNAUTHORIZED.value
    message = "Missing or invalid token."


class TokenExpiredError(UnauthorisedError):
    message = "Token has expired."


class ForbiddenError(APIError):
    status_code = HTTPStatus.FORBIDDEN.value
    message = "You do not have permission to access this resource."


class DuplicateError(APIError):
    status_code = HTTPStatus.CONFLICT.value
    message = "Resource already exists."


class TooManyRequestsError(APIError):
    status_code = HTTPStatus.TOO_MANY_REQUESTS.value
    message = "Too many requests. Please try again later."


def register_error_handlers(flask_app: Flask) -> None:
    # Local import to avoid circular import at module load time
    from app.extensions import jwt

    # Route-level APIError handler - catches anything raised in routes/services
    @flask_app.errorhandler(APIError)
    def handle_api_error(error: APIError):
        return jsonify(error.to_dict()), error.status_code

    # Werkzeug routing-level exceptions - raised before route functions run
    @flask_app.errorhandler(HTTPStatus.NOT_FOUND.value)
    def handle_not_found(error: HTTPException):
        return jsonify(NotFoundError().to_dict()), NotFoundError.status_code

    @flask_app.errorhandler(HTTPStatus.METHOD_NOT_ALLOWED.value)
    def handle_method_not_allowed(error: HTTPException):
        return jsonify(
            MethodNotAllowedError().to_dict()
        ), MethodNotAllowedError.status_code

    @flask_app.errorhandler(HTTPStatus.INTERNAL_SERVER_ERROR.value)
    def handle_internal_server_error(error: Exception):
        return jsonify(ServiceError().to_dict()), ServiceError.status_code

    @flask_app.errorhandler(HTTPStatus.UNPROCESSABLE_ENTITY.value)
    def handle_validation_error(error: UnprocessableEntity):
        # Override flask-smorest's default 422 handler to match our error shape.
        error_message = ValidationError.message

        messages = error.data.get("messages", {}).get("json", {})
        if messages:
            field_errors = list(messages.values())[0]
            error_message = field_errors[0]

        return jsonify(
            ValidationError(error_message).to_dict()
        ), ValidationError.status_code

    @flask_app.errorhandler(HTTPStatus.BAD_REQUEST.value)
    def handle_bad_request_error(error: BadRequest):
        """Handle malformed JSON and other bad requests."""

        return jsonify(
            ValidationError(
                "Invalid request.", status_code=HTTPStatus.BAD_REQUEST.value
            ).to_dict()
        ), HTTPStatus.BAD_REQUEST.value

    @flask_app.errorhandler(HTTPStatus.TOO_MANY_REQUESTS.value)
    def handle_rate_limit_exceeded(error: TooManyRequests):
        """Handle rate limit exceeded errors."""

        return jsonify(
            TooManyRequestsError().to_dict()
        ), TooManyRequestsError.status_code

    # JWT exceptions - intercepted before route functions run
    @jwt.unauthorized_loader
    def unauthorised_callback(reason: str):
        return jsonify(UnauthorisedError().to_dict()), UnauthorisedError.status_code

    @jwt.invalid_token_loader
    def invalid_token_callback(reason: str):
        return jsonify(UnauthorisedError().to_dict()), UnauthorisedError.status_code

    @jwt.expired_token_loader
    def expired_token_callback(jwt_header, jwt_payload):
        return jsonify(TokenExpiredError().to_dict()), TokenExpiredError.status_code
