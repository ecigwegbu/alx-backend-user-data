#!/usr/bin/env python3
""" Basic Auth Class - Inherits from Basic Authentication
"""
from api.v1.auth.auth import Auth
from base64 import b64decode
from models.user import User
from typing import Union, TypeVar


class BasicAuth(Auth):
    """ Manage the API Authentication
    """
    pass

    def extract_base64_authorization_header(self, authorization_header: str) \
            -> Union[str, None]:
        """ Return the Base64 part of the Authorization header for a Basic
            Authentication
        """
        base64_authorization_header = None
        if authorization_header and type(authorization_header) == str and \
                authorization_header.startswith("Basic "):
            base64_authorization_header = authorization_header[6:].strip()
        return base64_authorization_header

    def decode_base64_authorization_header(self, base64_authorization_header:
                                           str) -> Union[str, None]:
        """ Return the decoded value of a Base64 string
            base64_authorization_header
        """
        result = None  # 'username:password'
        if base64_authorization_header and \
                type(base64_authorization_header) == str:
            try:
                result = b64decode(base64_authorization_header).decode('utf-8')
            except Exception:
                result = None
        return result

    def extract_user_credentials(self, decoded_base64_authorization_header:
                                 str) -> (str, str):
        """ Return the user email and passwd from the Base64 decoded value
        """
        if decoded_base64_authorization_header is not None and \
                type(decoded_base64_authorization_header) == str and \
                ":" in decoded_base64_authorization_header:
            (email, password) = decoded_base64_authorization_header.split(
                                sep=":", maxsplit=1)
            return (email, password)
        return None, None

    def user_object_from_credentials(self, user_email: str, user_pwd: str) \
            -> TypeVar('User'):
        """ Return the Usr Instance based on his Email and Pasword
        """
        if (user_email is None) or (type(user_email) != str) or \
                (user_pwd is None) or (type(user_pwd) != str):
            return None
        if User.count() == 0:
            return None
        users = User.search({'email': user_email})
        if users:
            try:  # in cases of multiple password entries per email
                if users[0].is_valid_password(user_pwd):
                    return users[0]
            except Exception:
                pass
        return None

    def current_user(self, request=None) -> Union[TypeVar('User'), None]:
        """Return None - None - request will be the Flask request object
        """
        try:
            auth_header = self.authorization_header(request)
            base64_header = extract_base64_authorization_header(auth_header)
            decoded_header = decode_base64_authorization_header(base64_header)
            user_email, user_pwd = extract_user_credentials(decoded_header)
            user = user_object_from_credentials(user_email, user_pwd)
        except Exception:
            return None
        return user
