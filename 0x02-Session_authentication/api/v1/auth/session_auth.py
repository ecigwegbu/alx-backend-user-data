#!/usr/bin/env python3
""" Session Auth Class - Inherits from Basic Authentication
"""
from api.v1.auth.auth import Auth
from base64 import b64decode
from models.user import User
from typing import Union, TypeVar


class SessionAuth(Auth):
    """ Manage the API Authentication using Session object
    """
    pass
