import secrets
import string
from datetime import datetime, timezone

from app.extensions import db


def generate_short_code(length: int = 6) -> str:
    """Generate a cryptographically secure random short code."""
    alphabet = string.ascii_letters + string.digits
    return "".join(secrets.choice(alphabet) for _ in range(length))


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
