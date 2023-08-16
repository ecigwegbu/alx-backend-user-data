#!/usr/bin/env python3
"""Validate each end point of the app, using the requests module
"""
import requests


def register_user(email: str, password: str) -> None:
    """Register a new user based on email and password
    """
    url = "http://localhost:5000/users"
    data = {"email": EMAIL, "password": PASSWD}
    response = requests.post(url, data=data)
    assert response.status_code == 200
    payload = {"email": EMAIL, "message": "user created"}
    assert response.json() == payload


def log_in_wrong_password(email: str, password: str) -> None:
    """Login a user based on email and password. Create a
    session_id for the user, update the user in the database and
    add the session_id as a cookie to the response
    """
    url = "http://localhost:5000/sessions"
    data = {"email": EMAIL, "password": NEW_PASSWD}
    response = requests.post(url, data=data)
    assert response.status_code == 401


def profile_unlogged() -> None:
    """Get the user profile (email) based on a session_id cookie
    """
    url = "http://localhost:5000/profile"
    response = requests.get(url)
    assert response.status_code == 403


def log_in(email: str, password: str) -> str:
    """Login a user based on email and password. Create a
    session_id for the user, update the user in the database and
    add the session_id as a cookie to the response
    """
    url = "http://localhost:5000/sessions"
    data = {"email": EMAIL, "password": PASSWD}
    response = requests.post(url, data=data)
    if 'session_id' in response.cookies:
        session_id = response.cookies['session_id']
    else:
        session_id = None
    assert response.status_code == 200
    payload = {"email": EMAIL, "message": "logged in"}
    assert response.json() == payload
    return session_id


def profile_logged(session_id: str) -> None:
    """Get the user profile (email) based on a session_id cookie
    """
    url = "http://localhost:5000/profile"
    cookies = {"session_id": session_id}
    response = requests.get(url, cookies=cookies)
    payload = {"email": EMAIL}
    assert response.status_code == 200
    assert response.json() == payload


def log_out(session_id: str) -> None:
    """Logout the user: destroy the session ID and redirect the user
    to the welcome page - GET /
    """
    url = "http://localhost:5000/sessions"
    cookies = {"session_id": session_id}
    response = requests.delete(url, cookies=cookies)
    payload = {"message": "Bienvenue"}
    assert response.status_code == 200
    assert response.json() == payload


def reset_password_token(email: str) -> str:
    """Get a password reset token for a user based on the email
    """


def update_password(email: str, reset_token: str, new_password: str) -> None:
    """Update a user's password after verifying that the reset_token matches
    with the email
    """


EMAIL = "guillaume@holberton.io"
PASSWD = "b4l0u"
NEW_PASSWD = "t4rt1fl3tt3"


if __name__ == "__main__":

    register_user(EMAIL, PASSWD)
    log_in_wrong_password(EMAIL, NEW_PASSWD)
    profile_unlogged()
    session_id = log_in(EMAIL, PASSWD)
    profile_logged(session_id)
    log_out(session_id)
    # reset_token = reset_password_token(EMAIL)
    # update_password(EMAIL, reset_token, NEW_PASSWD)
    # log_in(EMAIL, NEW_PASSWD)
