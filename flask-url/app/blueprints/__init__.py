from flask import Flask

from app.extensions import api


def register_blueprints(flask_app: Flask) -> None:
    from app.blueprints.auth import auth_bp
    from app.blueprints.redirect import redirect_bp
    from app.blueprints.status import status_bp
    from app.blueprints.urls import urls_bp

    api.register_blueprint(status_bp)
    api.register_blueprint(auth_bp)
    api.register_blueprint(urls_bp)
    api.register_blueprint(redirect_bp)
