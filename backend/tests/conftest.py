import pytest

from app import create_app
from app.extensions import db
from app.models import SavedCity


@pytest.fixture
def app():
    application = create_app(
        {
            "TESTING": True,
            "SQLALCHEMY_DATABASE_URI": "sqlite:///:memory:",
            "USE_MOCK_WEATHER": True,
            "WEATHER_API_KEY": "",
        }
    )
    with application.app_context():
        db.create_all()
        yield application
        db.session.remove()
        db.drop_all()


@pytest.fixture
def client(app):
    return app.test_client()


@pytest.fixture
def saved_city(app):
    city = SavedCity(city_name="London", country="GB")
    db.session.add(city)
    db.session.commit()
    return city
