import secrets
import string
from datetime import datetime, timezone

from app.extensions import db


def generate_short_code(length: int = 6) -> str:
    """Generate a scryptographically secure random short code."""
    alphabet = string.ascii_letters + string.digits
    return "".join(secrets.choice(alphabet) for _ in range(length))


class URL(db.Model):
    __tablename__ = "url"

    id = db.Column(db.Integer, primary_key=True)
    original_url = db.Column(db.Text, nullable=False)
    short_code = db.Column(db.String(16), unique=True, nullable=False, index=True)
    clicks = db.Column(db.Integer, default=0, nullable=False)
    created_at = db.Column(
        db.DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        nullable=False,
    )

    def __repr__(self) -> str:
        return f"<URL {self.short_code} -> {self.original_url[:30]}>"

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "original_url": self.original_url,
            "short_code": self.short_code,
            "short_url": f"/{self.short_code}",
            "clicks": self.clicks,
            "created_at": self.created_at.isoformat(),
        }
