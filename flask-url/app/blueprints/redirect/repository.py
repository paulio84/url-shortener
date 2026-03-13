from sqlalchemy.exc import SQLAlchemyError

from app.errors import ServiceError
from app.extensions import db
from app.models.url import URL


class RedirectRepository:
    def get_by_short_code(self, short_code: str) -> URL | None:
        return URL.query.filter_by(short_code=short_code).first()

    def increment_clicks(self, url: URL) -> URL:
        try:
            url.clicks += 1
            db.session.commit()
            return url
        except SQLAlchemyError as e:
            db.session.rollback()
            raise ServiceError(f"Database error: {str(e)}")
