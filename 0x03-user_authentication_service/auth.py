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


def _generate_uuid() -> str:
    """Return a string representation of a new UUID
    """
    return str(uuid.uuid4())


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

    def create_session(self, email: str) -> str:
        """Return a Session ID based on a given email address.
        """
        # find user
        try:
            user = self._db.find_user_by(email=email)
        except NoResultFound:
            return None
        # generate UUID
        session_id = _generate_uuid()
        # Store UUID in database
        self._db.update_user(user.id, session_id=session_id)
        # Return Session ID
        return session_id

    def get_user_from_session_id(self, session_id: str) -> User:
        """Get a User based on a session_id
        """
        if session_id is None:
            return None
        try:
            user = self._db.find_user_by(session_id=session_id)
        except NoResultFound:
            return None
        return user

    def destroy_session(user_id: str) -> None:
        """Destroy a session by setting the session_id to none based on a
        given user_id
        """
        try:
            self._db.update_user(user_id, session_id=None)
        except NoResultFound:
            pass
