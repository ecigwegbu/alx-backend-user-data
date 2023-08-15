#!/usr/bin/env python3
"""Authorization module for the Flask App
"""
import bcrypt


def _hash_password(password: str) -> bytes:
    """Return a hashed version of a password
    """
    if type(password) != str:
        return None
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
