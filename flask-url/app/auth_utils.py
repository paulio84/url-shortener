from flask_jwt_extended import get_jwt_identity


def current_user_id() -> int:
    """Return the current authenticated user's ID from the JWT token."""

    return int(get_jwt_identity())
