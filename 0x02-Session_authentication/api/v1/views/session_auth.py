#!/usr/bin/env python3
"""Views to handle all routes for the Session authentication
"""
from api.v1.views import app_views
from flask import abort, jsonify, request
from models.user import User
import os
from typing import Any


@app_views.route('/auth_session/login', methods=['POST'], strict_slashes=False)
def create_session_user() -> str:
    """ POST /api/v1/auth_session/login
    JSON body:
      - email
      - password
      - last_name (optional)
      - first_name (optional)
    Return:
      - User object JSON represented
      - 400 if can't create the new User
    """
    # print(f"\n----sentry ---- printed?    \nUser Count: {User.count()}\n\n")
    user_email = request.form.get('email')
    user_pwd = request.form.get('password')
    if not user_email:
        return jsonify({"error": "email missing"}), 400
    if not user_pwd:
        return jsonify({"error": "password missing"}), 400
    if User.count() == 0:
        # print("\nHHHHH    HERE    \n")
        return jsonify({"error": "no user found for this email"}), 404
    # print(f"\nHHHHH  1 HERE    \n")
    users = User.search({'email': user_email})
    current_user = None
    # print(f"\nHHHHH  3 HERE    USERS:{users} \n")
    if not users:
        return jsonify({"error": "no user found for this email"}), 404
    try:  # in cases of multiple password entries per email
        # print(f"\nN%%%%%   BEFORE  Setting Current user:-{users[0]}--\n")
        if users[0].is_valid_password(user_pwd):
            # print(f"\nN%%%%% AFTER   Setting Current user:-------\n")
            current_user = users[0]
        else:
            # print(f"----------finished------------------------")
            return jsonify({"error": "wrong password"}), 401
    except Exception:
        # print("\nException:\n{e}")
        # exit(1)
        return jsonify({"error": "wrong password"}), 401

    # create a sessionID:
    # print(f"\n\n----????   111--------Current_user: {current_user}\n")
    from api.v1.app import auth
    # print(f"\n\n----????  222--------Current_user: {current_user}\n")
    session_id = auth.create_session(current_user.id)
    # print(f"\n\n----????  333--------Current_user: {current_user}\n")
    resp = jsonify(current_user.to_json())
    cookie_name = os.getenv("SESSION_NAME")
    resp.set_cookie(cookie_name, session_id)
    return resp, 200


@app_views.route('/auth_session/logout', methods=['DELETE'],
                 strict_slashes=False)
def delete_session() -> Any:
    """ DELETE /api/v1/auth_session/logout
    Path parameter:
      - None
    Return:
      - empty JSON is the session has been correctly deleted
      - 404 if the Session ID doesn't exist
    """
    from api.v1.app import auth
    if not auth.destroy_session(request):
        abort(404)
    return jsonify({}), 200
