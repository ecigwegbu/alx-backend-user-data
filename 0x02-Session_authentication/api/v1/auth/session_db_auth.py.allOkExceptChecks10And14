#!/usr/bin/env python3
"""Session Auth with data persistence to file"""
from api.v1.auth.session_exp_auth import SessionExpAuth
from models.user_session import UserSession
from datetime import datetime, timedelta
import os


class SessionDBAuth(SessionExpAuth):
    """Adds expiration feature to the Session Authentication app
    """
    def __init__(self):
        """Override base constructor
        """
        super().__init__()

    def create_session(self, user_id=None) -> str:
        """Create a session ID for a given user_id and make an entry with
            that session_id as key in the user_id_by_session_id dictionary
        """
        session_id = super().create_session(user_id)
        if not session_id:
            return None
        user = UserSession({'user_id': user_id, 'session_id': session_id})
        session_dictionary = {
               'user_id': user_id,
               'created_at': datetime.now()
        }
        self.user_id_by_session_id[session_id] = session_dictionary
        return session_id

    def user_id_for_session_id(self, session_id=None) -> str:
        """Lookup user_id based on a session_id, return a valid user_id
            if it has not expired, otherwise return None
        """
        if not session_id:
            return None
        session_dictionary = self.user_id_by_session_id.get(session_id)
        if not session_dictionary:
            return None
        user_id = session_dictionary.get('user_id')
        created_at = session_dictionary.get('created_at')
        if self.session_duration <= 0:
            return user_id
        if created_at is None:
            return None
        if created_at + timedelta(seconds=self.session_duration) < \
                datetime.now():
            return None
        return user_id

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
