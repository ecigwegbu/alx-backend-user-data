#!/usr/bin/env python3
"""
Route module for the API
"""
from os import getenv
from api.v1.views import app_views
from flask import Flask, jsonify, abort, request
from flask_cors import (CORS, cross_origin)
import os
from typing import Union, List


app = Flask(__name__)
app.register_blueprint(app_views)
CORS(app, resources={r"/api/v1/*": {"origins": "*"}})
auth = None


if getenv('AUTH_TYPE') == 'basic_auth':
    from api.v1.auth.basic_auth import BasicAuth
    auth = BasicAuth()
elif getenv('AUTH_TYPE') == 'auth':
    from api.v1.auth.auth import Auth
    auth = Auth()
elif getenv('AUTH_TYPE') == 'session_auth':
    from api.v1.auth.session_auth import SessionAuth
    auth = SessionAuth()


@app.errorhandler(404)
def not_found(error) -> str:
    """ Not found handler
    """
    return jsonify({"error": "Not found"}), 404


@app.errorhandler(401)
def unauthorized(error) -> str:
    """ Unauthorzed handler
    """
    return jsonify({"error": "Unauthorized"}), 401


@app.errorhandler(403)
def forbidden(error) -> str:
    """ Forbidden handler
    """
    return jsonify({"error": "Forbidden"}), 403


@app.before_request
def bf_request() -> Union[str, None]:
    """ Before every request - handler
    """
    # print("\n--1-Request path:\n", request.path,"\n----\n")  # debug
    excluded_paths = ['/api/v1/status/', '/api/v1/unauthorized/',
                      '/api/v1/forbidden/', '/api/v1/auth_session/login/']
    # print(f"--BEGIN--->> >> B4 request.")
    # print(f"request.path: {request.path}; excluded_paths: {excluded_paths}")
    # print(f"-- - - path in excl paths? {request.path in excluded_paths or
    # request.path + '/' in excluded_paths}")
    if (auth is not None) and \
            auth.require_auth(request.path, excluded_paths):
        # print("xxxxx !!!! Requires Auth: ", auth.require_auth(request.path,
        #                                                 excluded_paths))
        if auth.authorization_header(request) is None \
                and auth.session_cookie(request) is None:
            # print(f"\n-->> >> B4 request.\n")
            abort(401)  # unauthorized
        # print(f"HHHHH  HHHH Processing ... Requires Auth ....")
        # print(f"KKKK kkkk kKKKK  auth.current_user_email: {auth.current
        # user(request).email}")
        # print(f"KKKK kkkk kKKKK  auth.current_user_password:
        # {auth.current_user(request).password}")
        if auth.current_user(request) is None:
            # print(f"--403  auth.current_user(request) {auth.current
            # user(request)}")
            # print("\n*****Here******0\n")
            abort(403)  # authorized but forbidden
        request.current_user = auth.current_user(request)
        # print(f"\n CCCCCC  request.current_user_email: {request.current_user.
        # email}")
        # print(f"\nCCCCCC  request.current_user_password: {request.current
        # user.password}\n")


if __name__ == "__main__":
    host = getenv("API_HOST", "0.0.0.0")
    port = getenv("API_PORT", "5000")
    app.run(host=host, port=port, debug=True)
