from flask import Flask


def register_blueprints(flask_app: Flask) -> None:
    from app.blueprints.urls import urls_bp

    flask_app.register_blueprint(urls_bp)
