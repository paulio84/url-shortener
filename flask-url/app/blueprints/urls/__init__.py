from flask_smorest import Blueprint

urls_bp = Blueprint(
    "urls",
    __name__,
    url_prefix="/api",
    description="URL shortening and management endpoints",
)

from app.blueprints.urls import routes  # noqa: E402, F401
