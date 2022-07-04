"""This module encopassing function for validate requests for the auth system"""
from ..models.auth import User
from ..constants.http_status_codes import HTTP_400_BAD_REQUEST, HTTP_409_CONFLICT
from email_validator import validate_email as _validate_email, EmailNotValidError

def validate_username(username):
    """This function validates the username from request"""
    if not username:
        return {"error": "The field username is required", "status": HTTP_400_BAD_REQUEST}
    if " " in username:
        return {"error": "The field username can not contain spaces", "status": HTTP_400_BAD_REQUEST}
    if len(username) < 5:
        return {"error": "The field username need at least 5 characters", "status": HTTP_400_BAD_REQUEST}

    username_already_exists = User.query.filter_by(username=username).first()
    
    if username_already_exists is not None:
        return {"error": "Username already exists", "status": HTTP_409_CONFLICT}

    return None

def validate_email(email):
    """This function validates the email from request"""
    if not email:
        return {"error": "The field email is required", "status": HTTP_400_BAD_REQUEST}
    
    try:
        _validate_email(email)
    except EmailNotValidError:
        return {"error": "You need to type a valid email", "status": HTTP_400_BAD_REQUEST}
    
    email_already_registered = User.query.filter_by(email=email).first()

    if email_already_registered is not None:
        return {"error": "Email already registered", "status": HTTP_409_CONFLICT}

    return None

def validate_password(password, confirm_password):
    """This function validates the password and confirm_password from the request"""
    if not password:
        return {"error": "The field password is required", "status": HTTP_400_BAD_REQUEST}

    if not confirm_password:
        return {"error": "You need to confirm the password", "status": HTTP_400_BAD_REQUEST}

    if len(password) < 8:
        return {"error": "Password needs at least 8 characters", "status": HTTP_400_BAD_REQUEST}
    
    if password != confirm_password:
        return {"error": "Passwords do not match", "status": HTTP_400_BAD_REQUEST}

    return None
