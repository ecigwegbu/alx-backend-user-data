#!/usr/bin/python3
""" Check response
"""
from models.user_session import UserSession

if __name__ == "__main__":
    try:
        UserSession.load_from_file()
        nb_before = UserSession.count()

        from api.v1.auth.session_db_auth import SessionDBAuth
        sdba = SessionDBAuth()
        user_id = "User 6"
        session_id = sdba.create_session(user_id)
        if session_id is None:
            print("create_session should return a Session ID if user_id is valid")
            exit(1)
        
        # validate in DB
        UserSession.load_from_file()
        nb_after = UserSession.count()
        if nb_after != (nb_before + 1):
            print("create_session with a valid user_id should generate a UserSession object")
            exit(1)

        is_found = (len(UserSession.search({'user_id': user_id})) > 0)
        if not is_found:
            print("UserSession not found for this User ID ({}) and Session ID ({}): {}".format(user_id, session_id, UserSession.all()))
            exit(1)
        
        print("OK", end="")
    except:
        import sys
        print("Error: {}".format(sys.exc_info()))
