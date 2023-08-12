#!/usr/bin/env python3
""" Session Auth Class - Inherits from Basic Authentication
"""
from api.v1.auth.auth import Auth
from base64 import b64decode
from models.user import User
from typing import Union, TypeVar
import uuid


class SessionAuth(Auth):
    """ Manage the API Authentication using Session object
    """
    user_id_by_session_id = {}

    def create_session(self, user_id: str = None) -> str:
        """Create a Session ID (uuid) for a given user_id
        """
        if user_id is None or type(user_id) != str:
            return None
        session_id = str(uuid.uuid4())
        self.user_id_by_session_id[session_id] = user_id
        return session_id

    def user_id_for_session_id(self, session_id: str = None) -> str:
        """ Return (lookup) a User ID based on a Session ID
        """
        if session_id is None or type(session_id) != str:
            return None
        return self.user_id_by_session_id.get(session_id)

    # def current_user(self, request=None):
    def current_user(self, request=None) -> Union[TypeVar('User'), None]:
        """return a user instance based on a given cookie
        """
        try:
            # the cookie value is the session_id!!
            session_id = self.session_cookie(request)
            user_id = self.user_id_for_session_id(session_id)
            user = User.get(user_id)
        except Exception:
            # except Exception as e:
            # print(f"---> .... session_cookie\n {session_cookie} \n ")
            # print(f"---> .... Exception:\n {e} \n ")
            return None
        return user

    def destroy_session(self, request=None) -> bool:
        """Delete the user session / logout
        """
        if request is None:
            return False
        session_id = self.session_cookie(request)
        if session_id is None or \
                self.user_id_for_session_id(session_id) is None:
            return False
        if session_id not in self.user_id_by_session_id:
            return False
        self.user_id_by_session_id.pop(session_id)
        return True
