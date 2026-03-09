import os

from flask import Flask

from app.config import config
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

    # register blueprints
    register_blueprints(flask_app)

    return flask_app


def register_blueprints(flask_app: Flask) -> None:
    from app.blueprints.urls import urls_bp

    flask_app.register_blueprint(urls_bp)
