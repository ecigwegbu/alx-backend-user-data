#!/usr/bin/env python3
"""This module implements password encryption using bcrypt"""
import bcrypt


def hash_password(password: str) -> bytes:
    """Encripts a password and resturns a salted hashed password string"""
    utf8_encoded_password: bytes = password.encode("utf-8")
    return bcrypt.hashpw(utf8_encoded_password, bcrypt.gensalt())


def is_valid(hashed_password: bytes, password: str) -> bool:
    """Check if a password matches.
    If it does return True otherwise False"""
    return bcrypt.checkpw(password.encode("utf-8"), hashed_password)
