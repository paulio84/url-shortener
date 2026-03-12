from http import HTTPStatus

from flask.testing import FlaskClient


class TestRedirect:
    """Tests for GET /<short_code>"""

    def test_redirect_valid_short_code_returns_302(
        self, authenticated_client: FlaskClient
    ):
        post_response = authenticated_client.post(
            "/api/shorten", json={"url": "https://www.example.com"}
        )
        short_code = post_response.get_json()["short_code"]

        response = authenticated_client.get(f"/{short_code}", follow_redirects=False)

        assert response.status_code == HTTPStatus.FOUND

    def test_redirect_points_to_correct_url(self, authenticated_client: FlaskClient):
        post_response = authenticated_client.post(
            "/api/shorten", json={"url": "https://www.example.com"}
        )
        short_code = post_response.get_json()["short_code"]

        response = authenticated_client.get(f"/{short_code}", follow_redirects=False)

        assert response.location == "https://www.example.com"

    def test_redirect_increments_click_count(self, authenticated_client: FlaskClient):
        post_response = authenticated_client.post(
            "/api/shorten", json={"url": "https://www.example.com"}
        )
        short_code = post_response.get_json()["short_code"]

        authenticated_client.get(f"/{short_code}", follow_redirects=False)
        authenticated_client.get(f"/{short_code}", follow_redirects=False)

        url_response = authenticated_client.get(f"/api/urls/{short_code}")
        assert url_response.get_json()["clicks"] == 2

    def test_redirect_nonexistent_short_code_returns_404(self, client: FlaskClient):
        response = client.get("/doesnotexist", follow_redirects=False)
        assert response.status_code == HTTPStatus.NOT_FOUND

    def test_redirect_is_publicly_accessible(
        self, authenticated_client: FlaskClient, client: FlaskClient
    ):
        """Verify redirect works without authentication."""
        post_response = authenticated_client.post(
            "/api/shorten", json={"url": "https://www.example.com"}
        )
        short_code = post_response.get_json()["short_code"]

        response = client.get(f"/{short_code}", follow_redirects=False)

        assert response.status_code == HTTPStatus.FOUND
