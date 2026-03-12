from flask import Flask


def register_blueprints(flask_app: Flask) -> None:
    from app.blueprints.auth import auth_bp
    from app.blueprints.redirect import redirect_bp
    from app.blueprints.urls import urls_bp

    flask_app.register_blueprint(auth_bp)
    flask_app.register_blueprint(urls_bp)
    flask_app.register_blueprint(redirect_bp)
