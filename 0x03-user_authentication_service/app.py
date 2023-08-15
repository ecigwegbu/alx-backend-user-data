#!/usr/bin/env python3
"""
Basic Flask app that returns a BienVenue message
"""
from flask import Flask, jsonify, request, abort
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


@app.route("/sessions", methods=["POST"], strict_slashes=False)
def login():
    """Handle user login based on email and password. Create a
    session cookie
    """
    email = request.form.get("email")
    password = request.form.get("password")
    if not AUTH.valid_login(email, password):
        abort(401)
    session_id = AUTH.create_session(email)
    resp = jsonify({"email": email, "message": "logged in"})
    resp.set_cookie("session_id", session_id)
    return resp, 200


if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5000")
