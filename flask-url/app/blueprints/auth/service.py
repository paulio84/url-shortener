from app.blueprints.auth.repository import AuthRepository
from app.errors import NotFoundError, ValidationError
from app.extensions import bcrypt
from app.models.user import User


class AuthService:
    def __init__(self, repository: AuthRepository):
        self.repository = repository

    def register(self, email: str, password: str) -> User:
        if self.repository.get_by_email(email):
            raise ValidationError("An account with this email already exists.")

        password_hash = bcrypt.generate_password_hash(password).decode("utf-8")
        user = User(email=email, password_hash=password_hash)
        return self.repository.save(user)

    def login(self, email: str, password: str) -> User:
        user = self.repository.get_by_email(email)
        if not user or not bcrypt.check_password_hash(user.password_hash, password):
            raise NotFoundError("Invalid username or password.")

        return user
