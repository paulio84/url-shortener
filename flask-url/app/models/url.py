import base64
import hashlib
import secrets
from datetime import datetime, timezone

from app.extensions import db


def generate_short_code(original_url: str, user_id: int, length: int = 6) -> str:
    """
    Generate a short code using SHA256 hash with a random salt.

    Using a hash-based approach with a random salt avoids collistion-check
    loops and produces a uniform distribution across the character space.
    """
    salt = secrets.token_hex(8)
    content = f"{original_url}{user_id}{salt}"
    hash_bytes = hashlib.sha256(content.encode()).digest()
    return base64.urlsafe_b64encode(hash_bytes)[:length].decode()


class URL(db.Model):
    __tablename__ = "url"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(
        db.Integer, db.ForeignKey("user.id", ondelete="CASCADE"), nullable=False
    )
    original_url = db.Column(db.Text, nullable=False)
    short_code = db.Column(db.String(16), unique=True, nullable=False, index=True)
    clicks = db.Column(db.Integer, default=0, nullable=False)
    created_at = db.Column(
        db.DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        nullable=False,
    )

    user = db.relationship("User", back_populates="urls")

    def __repr__(self) -> str:
        return f"<URL {self.short_code} -> {self.original_url[:30]}>"
