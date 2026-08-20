import os
from pathlib import Path

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from dotenv import load_dotenv

BASE_DIR = Path(__file__).resolve().parent.parent
load_dotenv(BASE_DIR / ".env")

db = SQLAlchemy()


def create_app():
    app = Flask(__name__)

    database_url = os.getenv("DATABASE_URL")

    if not database_url:
        raise RuntimeError("DATABASE_URL was not found in .env")

    app.config["SQLALCHEMY_DATABASE_URI"] = database_url
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    db.init_app(app)

    from app.models import URL
    from app.routes import url_bp, redirect_bp

    app.register_blueprint(url_bp)
    app.register_blueprint(redirect_bp)

    with app.app_context():
        db.create_all()

    @app.route("/")
    def home():
        return {
            "message": "CodeAlpha URL Shortener API is running",
            "database": "PostgreSQL"
        }

    return app
