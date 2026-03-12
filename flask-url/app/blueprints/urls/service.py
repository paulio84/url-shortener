from app.blueprints.urls.repository import URLRepository
from app.errors import NotFoundError, ServiceError
from app.models.url import URL, generate_short_code


class URLService:
    def __init__(self, repository: URLRepository):
        self.repository = repository

    def create_short_url(self, original_url: str, user_id: int) -> URL:
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

        url = URL(original_url=original_url, short_code=code, user_id=user_id)
        return self.repository.save(url)

    def get_by_short_code_for_user(self, short_code: str, user_id: int) -> URL:
        url = self.repository.get_by_short_code_for_user(short_code, user_id)
        if not url:
            raise NotFoundError(f"Short code '{short_code}' not found.")
        return url

    def get_all_for_user(self, user_id: int) -> list[URL]:
        return self.repository.get_all_for_user(user_id)
