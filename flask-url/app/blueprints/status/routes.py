from http import HTTPStatus

from flask import jsonify

from app.blueprints.status import status_bp


@status_bp.get("/status")
@status_bp.response(HTTPStatus.OK)
def status():
    return jsonify({"status": "ok"}), HTTPStatus.OK.value
