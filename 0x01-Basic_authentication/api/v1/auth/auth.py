#!/usr/bin/env python3
""" Auth Class - Basic Authentication
"""
from flask import request
from typing import List, Union, TypeVar
from fnmatch import fnmatch


class Auth():
    """ Manage the API Authentication
    """

    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """Return False - path and excluded_paths will be used later
        now, you don’t need to take care of them.
        """
        # if path and excluded_paths and (path in excluded_paths or
        #                                 (path + "/") in excluded_paths):
        if path and excluded_paths and path_matches(path, excluded_paths):
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

    def path_matches(path: str, patterns: List[str]) -> bool:
        """match pathname against a pattern
        """
        for pattern in patterns:
            if fnmatch(path, pattern) or fnmatch(path + "/", pattern):
                return True
        return False
