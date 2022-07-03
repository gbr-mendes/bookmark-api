"""This module is responsible for encopassin the routes of the auth system"""
from flask import Blueprint
from ..constants.general_variables import MAIN_URL_PREFIX
from ..controllers import auth

auth_blueprint = Blueprint("auth", __name__, url_prefix=f"{MAIN_URL_PREFIX}/auth")

auth_blueprint.post("/register")(auth.register)
auth_blueprint.get("/me")(auth.me)
