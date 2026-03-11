from http import HTTPStatus

from flask.testing import FlaskClient


class TestShortenURL:
    """Tests for POST /api/shorten"""

    def test_shorten_valid_url_returns_201(self, client: FlaskClient):
        response = client.post("/api/shorten", json={"url": "https://www.example.com"})

        assert response.status_code == HTTPStatus.CREATED

    def test_shorten_valid_url_returns_expected_fields(self, client: FlaskClient):
        response = client.post("/api/shorten", json={"url": "https://www.example.com"})
        data = response.get_json()

        assert "id" in data
        assert "short_code" in data
        assert "short_url" in data
        assert "original_url" in data
        assert "clicks" in data
        assert "created_at" in data
        assert data["short_url"] == f"/{data['short_code']}"

    def test_shorten_valid_url_returns_correct_values(self, client: FlaskClient):
        response = client.post("/api/shorten", json={"url": "https://www.example.com"})
        data = response.get_json()

        assert data["original_url"] == "https://www.example.com"
        assert data["clicks"] == 0
        assert len(data["short_code"]) == 6

    def test_shorten_missing_url_field_returns_400(self, client: FlaskClient):
        response = client.post("/api/shorten", json={})

        assert response.status_code == HTTPStatus.BAD_REQUEST

    def test_shorten_missing_url_field_returns_error_shape(self, client: FlaskClient):
        response = client.post("/api/shorten", json={})
        data = response.get_json()

        assert "error" in data
        assert "status" in data["error"]
        assert "message" in data["error"]

    def test_shorten_invalid_url_returns_400(self, client: FlaskClient):
        response = client.post("/api/shorten", json={"url": "not-valid-url"})

        assert response.status_code == HTTPStatus.BAD_REQUEST

    def test_shorten_empty_body_returns_400(self, client: FlaskClient):
        response = client.post("/api/shorten", json={"url": ""})

        assert response.status_code == HTTPStatus.BAD_REQUEST

    def test_shorten_http_url_is_accepted(self, client: FlaskClient):
        response = client.post("/api/shorten", json={"url": "http://www.example.com"})

        assert response.status_code == HTTPStatus.CREATED


class TestListURLs:
    """Test for GET /api/urls"""

    def test_list_urls_returns_200(self, client: FlaskClient):
        response = client.get("/api/urls")

        assert response.status_code == HTTPStatus.OK

    def test_list_urls_returns_empty_list_when_no_urls(self, client: FlaskClient):
        response = client.get("/api/urls")
        data = response.get_json()

        assert data == []

    def test_list_urls_returns_created_urls(self, client: FlaskClient):
        client.post("/api/shorten", json={"url": "https://www.example.com"})
        client.post("/api/shorten", json={"url": "https://www.python.org"})

        response = client.get("/api/urls")
        data = response.get_json()

        assert len(data) == 2

    def test_list_urls_returns_list_of_expected_shape(self, client: FlaskClient):
        client.post("/api/shorten", json={"url": "https://www.example.com"})

        response = client.get("/api/urls")
        data = response.get_json()

        assert isinstance(data, list)
        assert "short_code" in data[0]


class TestGetURLByShortCode:
    """Tests for GET /api/urls/<short_code>"""

    def test_get_existing_url_returns_200(self, client: FlaskClient):
        post_response = client.post(
            "/api/shorten", json={"url": "https://www.example.com"}
        )
        short_code = post_response.get_json()["short_code"]

        response = client.get(f"/api/urls/{short_code}")

        assert response.status_code == HTTPStatus.OK

    def test_get_existing_url_returns_correct_data(self, client: FlaskClient):
        post_response = client.post(
            "/api/shorten", json={"url": "https://www.example.com"}
        )
        short_code = post_response.get_json()["short_code"]

        response = client.get(f"/api/urls/{short_code}")
        data = response.get_json()

        assert data["short_code"] == short_code
        assert data["original_url"] == "https://www.example.com"

    def test_get_nonexistent_url_returns_404(self, client: FlaskClient):
        response = client.get("/api/urls/doesnotexist")

        assert response.status_code == HTTPStatus.NOT_FOUND

    def test_get_nonexistent_url_returns_error_shape(self, client: FlaskClient):
        response = client.get("/api/urls/doesnotexist")
        data = response.get_json()

        assert "error" in data
        assert "status" in data["error"]
        assert "message" in data["error"]
