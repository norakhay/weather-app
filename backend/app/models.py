from datetime import datetime, timezone

from app.extensions import db


class SavedCity(db.Model):
    __tablename__ = "saved_cities"

    id = db.Column(db.Integer, primary_key=True)
    city_name = db.Column(db.String(100), nullable=False, unique=True)
    country = db.Column(db.String(10), nullable=True)
    created_at = db.Column(
        db.DateTime(timezone=True),
        nullable=False,
        default=lambda: datetime.now(timezone.utc),
    )

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "city_name": self.city_name,
            "country": self.country,
            "created_at": self.created_at.isoformat() if self.created_at else None,
        }
