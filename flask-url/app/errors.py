from http import HTTPStatus

from flask import Flask, jsonify
from werkzeug.exceptions import HTTPException


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
    status_code = HTTPStatus.BAD_REQUEST.value
    message = "Invalid request data."


class ServiceError(APIError):
    status_code = HTTPStatus.INTERNAL_SERVER_ERROR.value
    message = "An internal service error occurred."


class MethodNotAllowedError(APIError):
    status_code = HTTPStatus.METHOD_NOT_ALLOWED.value
    message = "Method not allowed."


def register_error_handlers(flask_app: Flask) -> None:
    @flask_app.errorhandler(APIError)
    def handle_api_error(error: APIError):
        return jsonify(error.to_dict()), error.status_code

    @flask_app.errorhandler(HTTPStatus.NOT_FOUND.value)
    def handle_not_found(error: HTTPException):
        return jsonify(NotFoundError().to_dict()), error.status_code

    @flask_app.errorhandler(HTTPStatus.METHOD_NOT_ALLOWED.value)
    def handle_method_not_allowed(error: HTTPException):
        return jsonify(MethodNotAllowedError().to_dict()), error.status_code

    @flask_app.errorhandler(HTTPStatus.INTERNAL_SERVER_ERROR.value)
    def handle_internal_server_error(error: HTTPException):
        return jsonify(ServiceError().to_dict()), error.status_code
