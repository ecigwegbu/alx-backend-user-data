#!/usr/bin/env python3
""" Auth Class - Basic Authentication
"""
from flask import request
from typing import List, Union, TypeVar


class Auth():
    """ Manage the API Authentication
    """

    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """Return False - path and excluded_paths will be used later
        now, you don’t need to take care of them.
        """
        return False

    def authorization_header(self, request=None) -> Union[str, None]:
        """Return None - None - request will be the Flask request object
        """
        return None

    def current_user(self, request=None) -> Union[TypeVar('User'), None]:
        """Return None - None - request will be the Flask request object
        """
        return None
