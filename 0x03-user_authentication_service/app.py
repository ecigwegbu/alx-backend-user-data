#!/usr/bin/env python3
"""
Basic Flask app that returns a BienVenue message
"""
from flask import Flask, jsonify, request, abort, url_for, redirect
from auth import Auth


AUTH = Auth()


app = Flask(__name__)


@app.route("/", methods=["GET"], strict_slashes=False)
def root_route() -> str:
    """ GET Home Page of the app
    Return:
        - Welcome Page
    """
    return jsonify({"message": "Bienvenue"}), 200


@app.route("/users", methods=["POST"], strict_slashes=False)
def users():
    """Implements the /users POST route
    """
    email = request.form.get("email")
    password = request.form.get("password")
    try:
        registered_user = AUTH.register_user(email, password)
        if registered_user:
            return jsonify({"email": email, "message": "user created"}), 200
        else:
            return jsonify({"message": "bad request"}), 400
    except ValueError:
        return jsonify({"message": "email already registered"}), 400
    pass


@app.route("/sessions", methods=["POST", "DELETE"], strict_slashes=False)
def login():
    """POST: Handle user login based on email and password. Create a
    session cookie
    DELETE: Destroy the session ID and redirect the user to GET /
    """
    if request.method == "POST":
        # print("\n-->-->Now in POST method\n")
        email = request.form.get("email")
        password = request.form.get("password")
        # print(f"\n------email: {email}, password: {password}\n")
        if not AUTH.valid_login(email, password):
            abort(401)
        session_id = AUTH.create_session(email)
        resp = jsonify({"email": email, "message": "logged in"})
        resp.set_cookie("session_id", session_id)
        return resp, 200
    elif request.method == "DELETE":
        # print("\n-->-->Now in DELETE method\n")
        session_id = request.cookies.get("session_id")
        if session_id:
            # print("\nDDDDDD    ", dir(AUTH))
            user = AUTH.get_user_from_session_id(session_id)
            if user:
                AUTH.destroy_session(user.id)
                return redirect(url_for("root_route"))
        abort(403)


@app.route("/profile", methods=["GET"], strict_slashes=False)
def profile():
    """Get the user profile (email) based on a session_id
    """
    session_id = request.cookies.get("session_id")
    if session_id:
        user = AUTH.get_user_from_session_id(session_id)
        if user:
            return jsonify({"email": user.email}), 200
    abort(403)


@app.route("/reset_password", methods=["POST"], strict_slashes=False)
def get_reset_password_token():
    """Get a password reset token for a user based on the email
    """
    email = request.form.get("email")
    if not email:
        abort(403)
    try:
        reset_token = AUTH.get_reset_password_token(email)
    except ValueError:
        abort(403)
    return jsonify({"email": email, "reset_token": reset_token}), 200


@app.route("/reset_password", methods=["PUT"], strict_slashes=False)
def update_password():
    """Update a user's password after verifying that the reset_token matches
    with the email
    """
    email = request.form.get("email")
    reset_token = request.form.get("reset_token")
    try:
        user = AUTH._db.find_user_by(email=email, reset_token=reset_token)
        AUTH.update_password(reset_token, password)
    except NoResultFound:
        abort(403)
    return jsonify({"email": email, "message": "Password updated"}), 200


if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5000")
