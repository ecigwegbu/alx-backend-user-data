#!/usr/bin/env python3
"""Authorization module for the Flask App
"""
import bcrypt
from db import DB
from user import User
from sqlalchemy.exc import InvalidRequestError
from sqlalchemy.orm.exc import NoResultFound
import uuid


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

    def register_user(self, email: str, password: str) -> User:
        """Register a user based on provided credentials
        """
        try:
            assert email and type(email) is str and \
                password and type(password) is str
        except AssertionError:
            return None
        try:
            user = self._db.find_user_by(email=email)
            raise ValueError("User {} already exists".format(email))
        except NoResultFound:
            # hash password:
            hashed_pwd = _hash_password(password)
            # register user:
            user = self._db.add_user(email=email, hashed_password=hashed_pwd)
        return user

    def valid_login(self, email: str, password: str) -> bool:
        """ Validate a given email and password against the password on record
        """
        try:
            user = self._db.find_user_by(email=email)
            return bcrypt.checkpw(password.encode("utf-8"),
                                  user.hashed_password)
        except Exception:
            return False

    def _generate_uuid(self) -> str:
        """Return a string representation of a new UUID
        """
        return str(uuid.uuid4())
