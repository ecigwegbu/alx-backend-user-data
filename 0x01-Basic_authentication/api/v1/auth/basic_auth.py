#!/usr/bin/env python3
""" Basic Auth Class - Inherits from Basic Authentication
"""
from api.v1.auth.auth import Auth
from base64 import b64decode
from typing import Union


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
        (email, password) = (None, None)
        if decoded_base64_authorization_header is not None and \
                type(decoded_base64_authorization_header) == str and \
                ":" in decoded_base64_authorization_header:
            (email, password) = decoded_base64_authorization_header.split(
                                sep=":", maxsplit=1)
            return (email, password)
