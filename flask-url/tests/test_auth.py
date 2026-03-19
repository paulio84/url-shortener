from http import HTTPStatus

from flask.testing import FlaskClient


class TestRegister:
    """Tests for POST /api/auth/register"""

    def test_register_valid_credentials_returns_201(self, client: FlaskClient):
        response = client.post(
            "/api/auth/register",
            json={"email": "test@example.com", "password": "testpassword"},
        )
        assert response.status_code == HTTPStatus.CREATED

    def test_register_returns_expected_fields(self, client: FlaskClient):
        response = client.post(
            "/api/auth/register",
            json={"email": "test@example.com", "password": "testpassword"},
        )
        data = response.get_json()

        assert "id" in data
        assert "email" in data
        assert "created_at" in data
        assert "password" not in data
        assert "password_hash" not in data

    def test_register_duplicate_email_returns_422(self, client: FlaskClient):
        client.post(
            "/api/auth/register",
            json={"email": "test@example.com", "password": "testpassword"},
        )
        response = client.post(
            "/api/auth/register",
            json={"email": "test@example.com", "password": "testpassword"},
        )
        assert response.status_code == HTTPStatus.UNPROCESSABLE_ENTITY

    def test_register_missing_email_returns_422(self, client: FlaskClient):
        response = client.post(
            "/api/auth/register",
            json={"password": "testpassword"},
        )
        assert response.status_code == HTTPStatus.UNPROCESSABLE_ENTITY

    def test_register_missing_password_returns_422(self, client: FlaskClient):
        response = client.post(
            "/api/auth/register",
            json={"email": "test@example.com"},
        )
        assert response.status_code == HTTPStatus.UNPROCESSABLE_ENTITY

    def test_register_short_password_returns_422(self, client: FlaskClient):
        response = client.post(
            "/api/auth/register",
            json={"email": "test@example.com", "password": "short"},
        )
        assert response.status_code == HTTPStatus.UNPROCESSABLE_ENTITY

    def test_register_invalid_email_returns_422(self, client: FlaskClient):
        response = client.post(
            "/api/auth/register",
            json={"email": "notanemail", "password": "testpassword"},
        )
        assert response.status_code == HTTPStatus.UNPROCESSABLE_ENTITY

    def test_register_malformed_json_returns_400_and_correct_shape(
        self, client: FlaskClient
    ):
        response = client.post(
            "/api/auth/register",
            data='{"email: "test@test.com", "password: "testpassword"}',
            content_type="application/json",
        )
        data = response.get_json()
        assert response.status_code == HTTPStatus.BAD_REQUEST
        assert "error" in data
        assert "status" in data["error"]
        assert "message" in data["error"]
        assert data["error"]["message"] == "Invalid request."


class TestLogin:
    """Tests for POST /api/auth/login"""

    def test_login_valid_credentials_returns_200(self, client: FlaskClient):
        client.post(
            "/api/auth/register",
            json={"email": "test@example.com", "password": "testpassword"},
        )
        response = client.post(
            "/api/auth/login",
            json={"email": "test@example.com", "password": "testpassword"},
        )
        assert response.status_code == HTTPStatus.OK

    def test_login_returns_expected_fields(self, client: FlaskClient):
        client.post(
            "/api/auth/register",
            json={"email": "test@example.com", "password": "testpassword"},
        )
        response = client.post(
            "/api/auth/login",
            json={"email": "test@example.com", "password": "testpassword"},
        )
        data = response.get_json()

        assert "access_token" in data
        assert "refresh_token" in data
        assert "user" in data

    def test_login_wrong_password_returns_404(self, client: FlaskClient):
        client.post(
            "/api/auth/register",
            json={"email": "test@example.com", "password": "testpassword"},
        )
        response = client.post(
            "/api/auth/login",
            json={"email": "test@example.com", "password": "wrongpassword"},
        )
        assert response.status_code == HTTPStatus.NOT_FOUND

    def test_login_nonexistent_email_returns_404(self, client: FlaskClient):
        response = client.post(
            "/api/auth/login",
            json={"email": "nobody@example.com", "password": "testpassword"},
        )
        assert response.status_code == HTTPStatus.NOT_FOUND

    def test_login_returns_error_shape_on_failure(self, client: FlaskClient):
        response = client.post(
            "/api/auth/login",
            json={"email": "nobody@example.com", "password": "testpassword"},
        )
        data = response.get_json()

        assert "error" in data
        assert "status" in data["error"]
        assert "message" in data["error"]


class TestRefresh:
    """Tests for POST /api/auth/refresh"""

    def test_refresh_returns_new_access_token(self, client: FlaskClient):
        client.post(
            "/api/auth/register",
            json={"email": "test@example.com", "password": "testpassword"},
        )
        login_response = client.post(
            "/api/auth/login",
            json={"email": "test@example.com", "password": "testpassword"},
        )
        refresh_token = login_response.get_json()["refresh_token"]

        client.environ_base["HTTP_AUTHORIZATION"] = f"Bearer {refresh_token}"
        response = client.post("/api/auth/refresh")

        assert response.status_code == HTTPStatus.OK
        assert "access_token" in response.get_json()

    def test_refresh_without_token_returns_401(self, client: FlaskClient):
        response = client.post("/api/auth/refresh")
        assert response.status_code == HTTPStatus.UNAUTHORIZED
