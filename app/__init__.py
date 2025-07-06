from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from .routes import main
from .models import db
from config import Config

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    # Initialize extensions
    db.init_app(app)

    # Register Blueprints
    app.register_blueprint(main)

    return app
