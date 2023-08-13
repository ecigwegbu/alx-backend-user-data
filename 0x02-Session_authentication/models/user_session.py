#!/usr/bin/env python3
""" User module for Session Authentication
"""
from models.base import Base


class UserSession(Base):
    """ User class
    """

    def __init__(self, *args: list, **kwargs: dict):
        """ Initialize a User instance
        """
        # print(f"-- -- -- In userSession kwargs: {kwargs}\n")
        super().__init__(*args, **kwargs)
        # print(f"-- AFter Super-- --kwargs : {kwargs}\n")
        self.user_id = kwargs.get('user_id')
        self.session_id = kwargs.get('session_id')
        # print(f"-- AFter Every: self.user_id: {self.user_id}\n")
        # print(f"-- AFter Every: self.session_id: {self.session_id}\n")
