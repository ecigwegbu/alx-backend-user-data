#!/usr/bin/env python3
"""This module implements password encryption using bcrypt"""
import bcrypt


def hash_password(password: str) -> bool:
    """Encripts a password and resturns a salted hashed password string"""
    utf8_encoded_password = password.encode("utf-8")
    return bcrypt.hashpw(utf8_encoded_password, bcrypt.gensalt())
