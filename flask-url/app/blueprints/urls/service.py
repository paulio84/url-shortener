from app.blueprints.urls.repository import URLRepository
from app.errors import NotFoundError, ServiceError
from app.models.url import URL, generate_short_code


class URLService:
    def __init__(self, repository: URLRepository):
        self.repository = repository

    def create_short_url(self, original_url: str) -> URL:
        """
        Create a new short URL entry.
        Handles short code collision with a retry loop.
        """
        max_attempts = 5
        for _ in range(max_attempts):
            code = generate_short_code()
            if not self.repository.get_by_short_code(code):
                break
        else:
            raise ServiceError("Failed to generate a unique short code.")

        url = URL(original_url=original_url, short_code=code)
        return self.repository.save(url)

    def get_by_short_code(self, short_code: str) -> URL:
        url = self.repository.get_by_short_code(short_code)
        if not url:
            raise NotFoundError(f"Short code '{short_code}' not found.")
        return url

    def get_all(self) -> list[URL]:
        return self.repository.all()
