from sqlalchemy.exc import SQLAlchemyError

from app.errors import ServiceError
from app.extensions import db
from app.models.url import URL


class URLRepository:
    def exists_by_short_code(self, short_code: str) -> bool:
        return URL.query.filter_by(short_code=short_code).first() is not None

    def get_by_short_code_for_user(self, short_code: str, user_id: int) -> URL | None:
        return URL.query.filter_by(short_code=short_code, user_id=user_id).first()

    def get_all_for_user(self, user_id: int) -> list[URL]:
        return (
            URL.query.filter_by(user_id=user_id).order_by(URL.created_at.desc()).all()
        )

    def save(self, url: URL) -> URL:
        try:
            db.session.add(url)
            db.session.commit()
            return url
        except SQLAlchemyError as e:
            db.session.rollback()
            raise ServiceError(f"Database error: {str(e)}")
