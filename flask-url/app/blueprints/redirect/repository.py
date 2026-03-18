from sqlalchemy import update
from sqlalchemy.exc import SQLAlchemyError

from app.errors import ServiceError
from app.extensions import db
from app.models.url import URL


class RedirectRepository:
    def get_by_short_code(self, short_code: str) -> URL | None:
        return URL.query.filter_by(short_code=short_code).first()

    def increment_clicks(self, url: URL) -> URL:
        try:
            db.session.execute(
                update(URL).where(URL.id == url.id).values(clicks=URL.clicks + 1)
            )
            db.session.commit()
            db.session.refresh(url)
            return url
        except SQLAlchemyError as e:
            db.session.rollback()
            raise ServiceError(f"Database error: {str(e)}")
