#!/usr/bin/env python3
"""Setup data files"""


class SessionExpAuth(SessionAuth):
    """Adds expiration feature to the Session Authentication app
    """
    def __init__(self):
        """Override base constructor
        """
        env = os.getenv("SESSION_DURATION")
        try:
            session_duration = int(env)
        except Exception:
            session_duration = 0

    def create_session(self, user_id=None):
        """Create a session ID for a given user_id
        """
        pass

    def user_id_for_session_id(self, session_id=None):
        """Lookup user_id based on a session_id
        """
        pass
