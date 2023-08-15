#!/usr/bin/env python3
"""Authorization module for the Flask App
"""
import bcrypt
from db import DB
from user import User


def _hash_password(password: str) -> bytes:
    """Return a hashed version of a password
    """
    if type(password) != str:
        return None
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

class Auth:
    """Auth class to interact with the authentication database.
    """

    def __init__(self):
        """Initialize a new Auth object
        """
        self._db = DB()

    def register_user(email: str, password: str) -> User:
        """Register a user based on provided credentials
        """
        :wq


