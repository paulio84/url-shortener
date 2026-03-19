from flask_smorest import Blueprint

status_bp = Blueprint(
    "status", __name__, url_prefix="/api", description="Health check endpoint"
)

from app.blueprints.status import routes  # noqa: E402, F401
