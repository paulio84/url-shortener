from flask_smorest import Blueprint

auth_bp = Blueprint(
    "auth", __name__, url_prefix="/api/auth", description="Authentication endpoints"
)

from app.blueprints.auth import routes  # noqa: E402, F401
