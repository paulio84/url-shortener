from app.blueprints.redirect.repository import RedirectRepository
from app.errors import NotFoundError
from app.models.url import URL


class RedirectService:
    def __init__(self, repository: RedirectRepository):
        self.repository = repository

    def resolve_short_code(self, short_code: str) -> URL:
        """Resolve a short code to its original URL and record the click."""

        url = self.repository.get_by_short_code(short_code)
        if not url:
            raise NotFoundError(f"Short code '{short_code}' not found.")
        return self.repository.increment_clicks(url)
