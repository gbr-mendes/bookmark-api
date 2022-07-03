"""This module is responsible for encopassing the routes of the bookmarks system"""
from flask import Blueprint
from ..constants.general_variables import MAIN_URL_PREFIX
from ..controllers import bookmarks

bookmarks_blueprint = Blueprint("bookmarks", __name__, url_prefix=f"{MAIN_URL_PREFIX}/bookmarks")

bookmarks_blueprint.get("/")(bookmarks.get_all)
