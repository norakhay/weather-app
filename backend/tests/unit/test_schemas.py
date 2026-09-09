import pytest

from app.errors import AppError, require_city_name


def test_city_name_required():
    with pytest.raises(AppError):
        require_city_name(None)


def test_city_name_rejects_short_name():
    with pytest.raises(AppError):
        require_city_name("A")


def test_city_name_accepts_valid_name():
    assert require_city_name("Amman") == "Amman"


def test_city_name_required_when_empty():
    with pytest.raises(AppError):
        require_city_name("")
