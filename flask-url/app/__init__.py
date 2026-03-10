import os

from flask import Flask

from app.blueprints import register_blueprints
from app.config import config
from app.errors import register_error_handlers
from app.extensions import db, migrate


def create_app(config_name: str | None = None) -> Flask:
    """Application factory."""
    if config_name is None:
        config_name = os.environ.get("FLASK_ENV", "development")

    flask_app = Flask(__name__)
    flask_app.config.from_object(config[config_name])

    # initialise extensions
    db.init_app(flask_app)
    migrate.init_app(flask_app, db)

    from app import models  # noqa: F401

    # register blueprints and errors
    register_blueprints(flask_app)
    register_error_handlers(flask_app)

    return flask_app
