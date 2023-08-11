#!/usr/bin/env python3
""" Auth Class - Basic Authentication
"""
from flask import request
from typing import List, Union, TypeVar
from fnmatch import fnmatch
import os


class Auth():
    """ Manage the API Authentication
    """

    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """Return False - path and excluded_paths will be used later
        now, you don’t need to take care of them.
        """
        if path and excluded_paths and self.path_matches(path, excluded_paths):
            return False
        return True

    def authorization_header(self, request=None) -> Union[str, None]:
        """Return None - None - request will be the Flask request object
        """
        if request is None:
            return None
        return request.headers.get("Authorization")

    def current_user(self, request=None) -> Union[TypeVar('User'), None]:
        """Return None - None - request will be the Flask request object
        """
        return None

    def path_matches(self, path: str, patterns: List[str]) -> bool:
        """match pathname against a pattern
        """
        for pattern in patterns:
            if fnmatch(path, pattern) or fnmatch(path + "/", pattern):
                return True
        return False

    def session_cookie(self, request=None):
        """Return a cookie value from a request
        """
        if request is None:
            return None
        cookie_name = os.getenv('SESSION_NAME', '_my_session_id')
        # print(f"\n ii  iii   ii  cookie_name: {cookie_name}")
        # print(f"\n--------- dict request: {request.__dict__}")
        cookie = request.cookies.get(cookie_name)
        return cookie
