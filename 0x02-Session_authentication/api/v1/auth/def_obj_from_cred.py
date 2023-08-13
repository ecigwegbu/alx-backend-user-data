    def user_object_from_credentials(self, user_email: str, user_pwd: str) \
            -> TypeVar('User'):
        """ Return the Usr Instance based on his Email and Pasword
        """
        if (not user_email) or (type(user_email) != str) or \
                (not user_pwd) or (type(user_pwd) != str):
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
