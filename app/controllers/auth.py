"""This module is resposible for encopassing all the controller of the auth system"""
from flask import request, jsonify
from flask_jwt_extended import create_access_token, create_refresh_token, jwt_required, get_jwt_identity
from werkzeug.security import check_password_hash, generate_password_hash

from ..models.auth import User
from ..constants.http_status_codes import HTTP_200_OK, HTTP_201_CREATED, HTTP_400_BAD_REQUEST, HTTP_415_UNSUPPORTED_MEDIA_TYPE, HTTP_500_INTERNAL_SERVER_ERROR
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
    

def login():
    """This function handle the login of the user retriving a JWT for a valid user"""
    data = request.json
    email = data.get("email", "")
    password = data.get("password", "")

    user = User.query.filter_by(email=email).first()

    if user:
        is_password_valid = check_password_hash(user.password, password)

        if is_password_valid:
            refresh = create_refresh_token(identity=user.id)
            access = create_access_token(identity=user.id)

            return {"refresh_token": refresh, "access_token": access}, HTTP_200_OK
    else:
        return {"error": "Email or password incorrect"}, HTTP_400_BAD_REQUEST


@jwt_required(refresh=True)
def refresh_token():
    """Controller for refresh the access token"""
    user_id = get_jwt_identity()
    access = create_access_token(identity=user_id)

    return {"access_token": access}, HTTP_200_OK

@jwt_required()
def me():
    """This function is resposible get the logged user info"""
    user_id = get_jwt_identity()
    try:
        user = User.query.filter_by(id=user_id).first()
        return {
            "id": user.id,
            "username": user.username,
            "email": user.email
        }, HTTP_200_OK
    except Exception:
        return {"error": "An error has occurred when retriving the user"}, HTTP_500_INTERNAL_SERVER_ERROR
