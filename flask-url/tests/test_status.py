from http import HTTPStatus

from flask.testing import FlaskClient


class TestStatus:
    """Tests for GET /api/status"""

    def test_status_returns_200(self, client: FlaskClient):
        response = client.get("/api/status")

        assert response.status_code == HTTPStatus.OK

    def test_status_returns_expected_fields(self, client: FlaskClient):
        response = client.get("/api/status")
        data = response.get_json()

        assert "status" in data

    def test_status_returns_expected_value(self, client: FlaskClient):
        response = client.get("/api/status")
        data = response.get_json()

        assert data["status"] == "ok"

    def test_status_is_public(self, client: FlaskClient):
        """Status endpoint requires no authentication."""

        response = client.get("/api/status")
        assert response.status_code != HTTPStatus.UNAUTHORIZED
