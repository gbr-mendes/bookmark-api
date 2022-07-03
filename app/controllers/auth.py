"""This module is resposible for encopassing all the controller of the auth system"""
from flask import request, jsonify
from werkzeug.security import check_password_hash, generate_password_hash

from ..models.auth import User
from ..constants.http_status_codes import HTTP_400_BAD_REQUEST, HTTP_415_UNSUPPORTED_MEDIA_TYPE
from ..utils import auth_validation
from ..database.db import db

def register():
    """This function is responsible for create a new user"""
    data = request.json

    if not data:
        return {"error": "You need to pass a valid payload"}, HTTP_415_UNSUPPORTED_MEDIA_TYPE
    
    username = data.get("username")
    email = data.get("email")
    password = data.get("password")
    confirm_password = data.get("confirm_password")

    username_is_invalid = auth_validation.validate_username(username)
    password_is_invalid = auth_validation.validate_password(password, confirm_password)
    email_is_invalid = auth_validation.validate_email(email)

    if username_is_invalid is not None:
        return {"error": username_is_invalid["error"]}, username_is_invalid["status"]

    if password_is_invalid is not None:
        return {"error": password_is_invalid["error"]}, password_is_invalid["status"]
    
    if email_is_invalid is not None:
        return {"error": email_is_invalid["error"]}, email_is_invalid["status"]

    hashed_password = generate_password_hash(password)

    try:
        user = User(username=username, password=hashed_password, email=email)
        db.session.add(user)
        db.session.commit()
        return {"success": "User Created"}, 201
    except Exception:
        return {"error": "An unexpected error has occured"}, 500
    


def me():
    """This function is resposible get the logged user info"""
    return {"user": "me"}
