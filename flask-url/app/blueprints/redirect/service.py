import logging

from app.blueprints.redirect.repository import RedirectRepository
from app.errors import NotFoundError
from app.models.url import URL

logger = logging.getLogger(__name__)


class RedirectService:
    def __init__(self, repository: RedirectRepository):
        self.repository = repository

    def resolve_short_code(self, short_code: str) -> URL:
        """Resolve a short code to its original URL and record the click."""

        url = self.repository.get_by_short_code(short_code)
        if not url:
            logger.warning("Redirect attempted for unknown short code: %s", short_code)
            raise NotFoundError(f"Short code '{short_code}' not found.")
        resolved = self.repository.increment_clicks(url)
        logger.info(
            "Redirect resolved: %s -> %s (clicks=%d)",
            short_code,
            resolved.original_url,
            resolved.clicks,
        )
        return resolved
