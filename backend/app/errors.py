from flask import jsonify
from werkzeug.exceptions import HTTPException


class AppError(Exception):
    def __init__(self, message: str, status_code: int = 400):
        super().__init__(message)
        self.message = message
        self.status_code = status_code


def success(data, status: int = 200):
    return jsonify({"success": True, "data": data}), status


def fail(message: str, status: int):
    return jsonify({"success": False, "error": message}), status


def require_city_name(value) -> str:
    if value is None or not str(value).strip():
        raise AppError("City name is required", 400)
    name = str(value).strip()
    if len(name) < 2 or len(name) > 100:
        raise AppError("City name must be between 2 and 100 characters", 400)
    return name


def register_error_handlers(app):
    @app.errorhandler(AppError)
    def handle_app_error(exc: AppError):
        return fail(exc.message, exc.status_code)

    @app.errorhandler(Exception)
    def handle_unexpected(exc: Exception):
        if isinstance(exc, HTTPException):
            raise exc
        return fail("Unexpected server error", 500)
