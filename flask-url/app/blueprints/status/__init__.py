from flask import Blueprint

status_bp = Blueprint("status", __name__, url_prefix="/api")

from app.blueprints.status import routes  # noqa: E402, F401
