from sqlalchemy.exc import IntegrityError, SQLAlchemyError

from app.errors import DuplicateError, ServiceError
from app.extensions import db
from app.models.user import User


class AuthRepository:
    def get_by_email(self, email: str) -> User | None:
        return User.query.filter_by(email=email).first()

    def save(self, user: User) -> User:
        try:
            db.session.add(user)
            db.session.commit()
            return user
        except IntegrityError:
            db.session.rollback()
            raise DuplicateError()
        except SQLAlchemyError as e:
            db.session.rollback()
            raise ServiceError(f"Database error: {str(e)}")
