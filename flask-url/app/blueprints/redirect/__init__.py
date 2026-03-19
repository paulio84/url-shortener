from flask_smorest import Blueprint

redirect_bp = Blueprint("redirect", __name__, description="URL redirect endpoint")

from app.blueprints.redirect import routes  # noqa: E402, F401
