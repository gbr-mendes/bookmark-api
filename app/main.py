"""This module is the entry point of the application"""
import os
from datetime import timedelta
from flask import Flask
from flask_jwt_extended import JWTManager

#database import
from .database.db import db

#blueprints imports
from .routes.auth import auth_blueprint
from .routes.bookmarks import bookmarks_blueprint

def create_app(test_config=None):
    """This function is responsible to create an instance of the application and return it"""
    app = Flask(__name__, instance_relative_config=True)

    if test_config is None:
        app.config.from_mapping(
            SECRET_KEY=os.getenv("SECRET_KEY"),
            SQLALCHEMY_DATABASE_URI=os.getenv("DATABASE_URI"),
            JWT_SECRET_KEY=os.getenv("JWT_SECRET_KEY"),
            JWT_ACCESS_TOKEN_EXPIRES=timedelta(days=15)
        )
    else:
        app.config.from_mapping(test_config)
    
    db.app = app
    db.init_app(app)
    db.create_all()

    JWTManager(app)

    app.register_blueprint(auth_blueprint)
    app.register_blueprint(bookmarks_blueprint)

    return app
