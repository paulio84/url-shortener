import logging

from app.blueprints.urls.repository import URLRepository
from app.errors import NotFoundError, ServiceError
from app.models.url import URL, generate_short_code

# Create a logger named after the module - app.blueprints.urls.service.
# Useful in production logs to identify where the message came from.
logger = logging.getLogger(__name__)


class URLService:
    def __init__(self, repository: URLRepository):
        self.repository = repository

    def create_short_url(self, original_url: str, user_id: int) -> URL:
        """Create a new short URL entry. Handles short code collision with a retry loop."""

        max_attempts = 5
        for attempt in range(max_attempts):
            code = generate_short_code()
            if not self.repository.exists_by_short_code(code):
                break
            logger.warning(
                "Short code collision on attempt %d for user_id=%s",
                attempt + 1,
                user_id,
            )
        else:
            logger.error(
                "Failed to generate unique short code after %d attempts for user_id=%s",
                max_attempts,
                user_id,
            )
            raise ServiceError("Failed to generate a unique short code.")

        url = URL(original_url=original_url, short_code=code, user_id=user_id)
        saved_url = self.repository.save(url)
        logger.info("URL shortened: %s -> %s (user_id=%s)", original_url, code, user_id)
        return saved_url

    def get_by_short_code_for_user(self, short_code: str, user_id: int) -> URL:
        """Retrieve a URL by short code scoped to the current user."""

        url = self.repository.get_by_short_code_for_user(short_code, user_id)
        if not url:
            logger.warning(
                "URL not found: short_code=%s, user_id=%s", short_code, user_id
            )
            raise NotFoundError(f"Short code '{short_code}' not found.")
        return url

    def get_all_for_user(self, user_id: int) -> list[URL]:
        """Retrieve all URLs belonging to the current user."""
        urls = self.repository.get_all_for_user(user_id)
        logger.info("Fetched %d URLs for user_id=%s", len(urls), user_id)
        return urls
