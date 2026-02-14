import os

from flask import Flask
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()
migrate = Migrate()


def create_app():
    app = Flask(__name__)
    app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get("DATABASE_URL", "sqlite:///project.db")
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    # Keep a non-empty default so API key validation is active out of the box.
    app.config["FLASK_API_KEY"] = os.environ.get("FLASK_API_KEY", "my-super-secret-api-key")

    db.init_app(app)
    migrate.init_app(app, db)

    from .routes import api_bp

    app.register_blueprint(api_bp, url_prefix="/api")

    return app
