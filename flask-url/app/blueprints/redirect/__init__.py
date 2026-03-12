from flask import Blueprint

redirect_bp = Blueprint("redirect", __name__)

from app.blueprints.redirect import routes  # noqa: E402, F401
