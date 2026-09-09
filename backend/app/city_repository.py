from sqlalchemy import func
from sqlalchemy.exc import IntegrityError, SQLAlchemyError

from app.errors import AppError
from app.extensions import db
from app.models import SavedCity


class CityRepository:
    def list_all(self) -> list[SavedCity]:
        try:
            return SavedCity.query.order_by(SavedCity.created_at.desc()).all()
        except SQLAlchemyError as exc:
            raise AppError("Database error", 500) from exc

    def get_by_id(self, city_id: int) -> SavedCity:
        city = db.session.get(SavedCity, city_id)
        if city is None:
            raise AppError("Saved city not found", 404)
        return city

    def find_by_name(self, city_name: str) -> SavedCity | None:
        return SavedCity.query.filter(func.lower(SavedCity.city_name) == city_name.lower()).first()

    def create(self, city_name: str, country: str | None) -> SavedCity:
        city = SavedCity(city_name=city_name, country=country)
        db.session.add(city)
        return self._commit(city)

    def update(self, city: SavedCity, city_name: str, country: str | None) -> SavedCity:
        city.city_name = city_name
        city.country = country
        return self._commit(city)

    def delete(self, city: SavedCity) -> None:
        db.session.delete(city)
        self._commit(None)

    def _commit(self, city: SavedCity | None) -> SavedCity | None:
        try:
            db.session.commit()
        except IntegrityError as exc:
            db.session.rollback()
            raise AppError("City is already saved", 409) from exc
        except SQLAlchemyError as exc:
            db.session.rollback()
            raise AppError("Database error", 500) from exc
        return city
