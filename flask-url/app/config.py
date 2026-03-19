import os
from datetime import timedelta


class BaseConfig:
    """Shared configuration for all environments."""

    SQLALCHEMY_TRACK_MODIFICATIONS = False
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(hours=1)
    JWT_REFRESH_TOKEN_EXPIRES = timedelta(days=30)

    SECRET_KEY = os.environ.get("SECRET_KEY")
    JWT_SECRET_KEY = os.environ.get("JWT_SECRET_KEY")

    # OpenAPI configuration
    API_TITLE = "UrlMe API"
    API_VERSION = "v1"
    OPENAPI_VERSION = "3.0.3"
    OPENAPI_URL_PREFIX = "/"
    OPENAPI_SWAGGER_UI_PATH = "/api/docs"
    OPENAPI_SWAGGER_UI_URL = "https://cdn.jsdelivr.net/npm/swagger-ui-dist/"
    API_SPEC_OPTIONS = {
        "components": {
            "securitySchemes": {
                "bearerAuth": {
                    "type": "http",
                    "scheme": "bearer",
                    "bearerFormat": "JWT",
                }
            }
        }
    }

    @classmethod
    def validate(cls):
        required = ["SECRET_KEY", "JWT_SECRET_KEY"]
        missing = [key for key in required if not os.environ.get(key)]
        if missing:
            raise RuntimeError(
                f"Missing required environment variables: {', '.join(missing)}. "
                "Check your .env file or environment configuration."
            )


class DevelopmentConfig(BaseConfig):
    NAME = "development"
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = os.environ.get(
        "DATABASE_URL",
        "postgresql://postgres:postgres@localhost:5432/urlme_dev",
    )


class TestingConfig(BaseConfig):
    NAME = "testing"
    TESTING = True
    JWT_ACCESS_TOKEN_EXPIRES = False
    SQLALCHEMY_DATABASE_URI = os.environ.get(
        "TEST_DATABASE_URL",
        "postgresql://postgres:postgres@localhost:5433/urlme_test",
    )


class ProductionConfig(BaseConfig):
    NAME = "production"
    DEBUG = False
    SQLALCHEMY_DATABASE_URI = os.environ.get("DATABASE_URL")

    @classmethod
    def validate(cls):
        super().validate()

        required = ["DATABASE_URL"]
        missing = [key for key in required if not os.environ.get(key)]
        if missing:
            raise RuntimeError(
                f"Missing required environment variables: {', '.join(missing)}. "
                "Set these in your production environment."
            )


config = {
    DevelopmentConfig.NAME: DevelopmentConfig,
    TestingConfig.NAME: TestingConfig,
    ProductionConfig.NAME: ProductionConfig,
}
