import logging
import os

from flask import Flask

from app.blueprints import register_blueprints
from app.config import BaseConfig, DevelopmentConfig, config
from app.errors import register_error_handlers
from app.extensions import api, bcrypt, cors, db, jwt, migrate


def create_app(config_name: str | None = None) -> Flask:
    """Application factory."""
    if config_name is None:
        config_name = os.environ.get("FLASK_ENV", DevelopmentConfig.NAME)

    config_class: BaseConfig = config[config_name]
    config_class.validate()

    flask_app = Flask(__name__)
    flask_app.config.from_object(config_class)

    # Configure logging
    logging.basicConfig(
        level=logging.INFO, format="%(asctime)s %(levelname)s %(name)s: %(message)s"
    )

    # Initialise extensions
    db.init_app(flask_app)
    migrate.init_app(flask_app, db)
    jwt.init_app(flask_app)
    bcrypt.init_app(flask_app)
    cors.init_app(
        flask_app,
        resources={
            r"/api/*": {
                "origins": os.environ.get("CORS_ALLOWED_ORIGINS", "").split(",")
            }
        },
    )
    api.init_app(flask_app)

    from app import models  # noqa: F401

    # Register blueprints and errors
    register_error_handlers(flask_app)
    register_blueprints(flask_app)

    return flask_app
