from pathlib import Path

from dotenv import load_dotenv
from flask import Flask
from flask_cors import CORS

from app.errors import register_error_handlers
from app.extensions import db
from app.models import SavedCity
from app.routes import api


def create_app(config_overrides: dict | None = None) -> Flask:
    load_dotenv(Path(__file__).resolve().parents[1].parent / ".env")

    app = Flask(__name__)
    app.config.from_object("app.config.Config")
    if config_overrides:
        app.config.update(config_overrides)

    CORS(app, origins=app.config["FRONTEND_ORIGIN"])
    db.init_app(app)
    register_error_handlers(app)
    app.register_blueprint(api)

    with app.app_context():
        db.create_all()

    return app
