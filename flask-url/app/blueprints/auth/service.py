import logging

from app.blueprints.auth.repository import AuthRepository
from app.errors import NotFoundError, ValidationError
from app.extensions import bcrypt
from app.models.user import User

logger = logging.getLogger(__name__)  # g variable?


class AuthService:
    def __init__(self, repository: AuthRepository):
        self.repository = repository

    def register(self, email: str, password: str) -> User:
        """Register a new user account."""

        if self.repository.get_by_email(email):
            logger.warning("Registration attempt with existing email: %s", email)
            raise ValidationError("An account with this email already exists.")

        password_hash = bcrypt.generate_password_hash(password).decode("utf-8")
        user = User(email=email, password_hash=password_hash)
        saved_user = self.repository.save(user)
        logger.info("New user registered: %s (id=%s)", email, saved_user.id)
        return saved_user

    def login(self, email: str, password: str) -> User:
        """Authenticate a user and return the user object."""

        user = self.repository.get_by_email(email)
        if not user or not bcrypt.check_password_hash(user.password_hash, password):
            logger.warning("Failed login attempt for email: %s", email)
            raise NotFoundError("Invalid email or password.")

        logger.info("User logged in: %s (id=%s)", email, user.id)
        return user
