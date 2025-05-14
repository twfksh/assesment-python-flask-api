from flask import Blueprint, jsonify, request
from flask_jwt_extended import (
    create_access_token,
    get_jwt,
    jwt_required,
    get_jwt_identity,
    set_access_cookies,
    set_refresh_cookies,
    unset_jwt_cookies,
)
from pydantic import ValidationError

from database import engine
from schemas import UserSchema
from services import AuthService, UserService


auth_service = AuthService(engine)
user_service = UserService(engine)

auth_blueprint = Blueprint("auth", __name__)
user_blueprint = Blueprint("users", __name__)


@auth_blueprint.post("/register")
def register_user():
    """
    Register a new user.
    """
    data = request.get_json()
    try:
        user_data = UserSchema(**data)
    except ValidationError as e:
        return jsonify({"msg": str(e)}), 400

    username, password = user_data.username, user_data.password

    if not username or not password:
        return jsonify({"msg": "Missing username or password"}), 400

    try:
        new_user = user_service.create_user(username, password)
        return jsonify(
            {
                "msg": "User created successfully",
                "username": new_user.username,
                "created_at": new_user.created_at,
            }
        ), 201
    except Exception as e:
        return jsonify({"msg": str(e)}), 400


@auth_blueprint.post("/login")
def login_user():
    """
    Login a user by username and password.
    """
    data = request.get_json()
    try:
        user_data = UserSchema(**data)
    except ValidationError as e:
        return jsonify({"msg": str(e)}), 400

    username, password = user_data.username, user_data.password

    if not username or not password:
        return jsonify({"msg": "Missing username or password"}), 400

    try:
        tokens = auth_service.login(username, password)
        response = jsonify(tokens)
        set_access_cookies(response, tokens["access_token"])
        set_refresh_cookies(response, tokens["refresh_token"])

        return response, 200

    except Exception as e:
        return jsonify({"msg": str(e)}), 401


@auth_blueprint.get("/whoami")
@jwt_required()
def whoami():
    """
    Get the current user's information.
    """
    current_user = get_jwt_identity()
    try:
        user = user_service.get_user(current_user)
        return jsonify(
            {
                "username": user.username,
                "created_at": user.created_at,
            }
        ), 200
    except Exception as e:
        return jsonify({"msg": str(e)}), 401


@auth_blueprint.get("/refresh")
@jwt_required(refresh=True)
def refresh():
    """
    Refresh the access token using the refresh token.
    """
    current_user = get_jwt_identity()
    access_token = create_access_token(identity=current_user)
    response = jsonify({"access_token": access_token})
    set_access_cookies(response, access_token)
    return response, 200


@auth_blueprint.get("/logout")
@jwt_required()
def logout():
    """
    Logout the user by invalidating the refresh token.
    """
    jti = get_jwt()["jti"]
    auth_service.logout(jti)
    response = jsonify({"msg": "Successfully logged out"})
    unset_jwt_cookies(response)
    return response, 200


@user_blueprint.get("/all")
@jwt_required()
def get_all_users():
    """
    Get all users in the database.
    """
    try:
        users = user_service.get_users()
        return jsonify(
            [
                {"username": user.username, "created_at": user.created_at}
                for user in users
            ]
        ), 200
    except Exception as e:
        return jsonify({"msg": str(e)}), 500
