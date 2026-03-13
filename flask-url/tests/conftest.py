import pytest
from flask import Flask

from app import create_app
from app.config import TestingConfig
from app.extensions import db as _db


@pytest.fixture(scope="session")
def test_app():
    """Session-scoped test_app fixture
    Created once for the entire test session."""
    test_app = create_app(TestingConfig.NAME)

    with test_app.app_context():
        _db.create_all()
        yield test_app
        _db.drop_all()


@pytest.fixture(scope="function")
def client(test_app: Flask):
    """Function-scoped test client.
    Each test gets a clean client."""
    return test_app.test_client()


@pytest.fixture(scope="function")
def authenticated_client(test_app: Flask):
    """A test client with a valid JWT token pre-configured."""
    client = test_app.test_client()
    client.post(
        "/api/auth/register",
        json={"email": "test@example.com", "password": "testpass"},
    )

    response = client.post(
        "/api/auth/login",
        json={"email": "test@example.com", "password": "testpass"},
    )

    token = response.get_json()["access_token"]
    client.environ_base["HTTP_AUTHORIZATION"] = f"Bearer {token}"

    return client


@pytest.fixture(scope="function", autouse=True)
def clean_db(test_app: Flask):
    """Truncates all tables between tests."""

    with test_app.app_context():
        yield

        for table in reversed(_db.metadata.sorted_tables):
            _db.session.execute(table.delete())
        _db.session.commit()
