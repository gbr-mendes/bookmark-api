"""This module is the entry point of the application"""
import os
from flask import Flask

#blueprints imports
from .routes.auth import auth_blueprint
from .routes.bookmarks import bookmarks_blueprint

def create_app(test_config=None):
    """This function is responsible to create an instance of the application and return it"""
    app = Flask(__name__, instance_relative_config=True)

    if test_config is None:
        app.config.from_mapping(
            SECRET_KEY=os.getenv("SECRET_KEY")
        )
    else:
        app.config.from_mapping(test_config)
    
    app.register_blueprint(auth_blueprint)
    app.register_blueprint(bookmarks_blueprint)

    return app
