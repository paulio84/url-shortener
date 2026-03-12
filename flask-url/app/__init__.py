import os

from flask import Flask

from app.blueprints import register_blueprints
from app.config import DevelopmentConfig, ProductionConfig, config
from app.errors import register_error_handlers
from app.extensions import bcrypt, db, jwt, migrate


def create_app(config_name: str | None = None) -> Flask:
    """Application factory."""
    if config_name is None:
        config_name = os.environ.get("FLASK_ENV", DevelopmentConfig.NAME)

    if config_name == ProductionConfig.NAME:
        ProductionConfig.validate()

    flask_app = Flask(__name__)
    flask_app.config.from_object(config[config_name])

    # Initialise extensions
    db.init_app(flask_app)
    migrate.init_app(flask_app, db)
    jwt.init_app(flask_app)
    bcrypt.init_app(flask_app)

    from app import models  # noqa: F401

    # Register blueprints and errors
    register_error_handlers(flask_app)
    register_blueprints(flask_app)

    return flask_app
