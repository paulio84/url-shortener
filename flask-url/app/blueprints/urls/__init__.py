from flask import Blueprint

urls_bp = Blueprint("urls", __name__, url_prefix="/api")

from app.blueprints.urls import routes  # noqa: E402, F401
