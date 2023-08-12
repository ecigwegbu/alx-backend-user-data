#!/usr/bin/env python3
"""Setup data files"""
from api.v1.auth.session_auth import SessionAuth
from models.user import User
from datetime import datetime, timedelta
import os


class SessionExpAuth(SessionAuth):
    """Adds expiration feature to the Session Authentication app
    """
    def __init__(self):
        """Override base constructor
        """
        env = os.getenv("SESSION_DURATION")
        try:
            self.session_duration = int(env)
        except Exception:
            self.session_duration = 0

    def create_session(self, user_id=None) -> str:
        """Create a session ID for a given user_id and make an entry with
            that session_id as key in the user_id_by_session_id dictionary
        """
        session_id = super().create_session(user_id)
        if not session_id:
            return None
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
