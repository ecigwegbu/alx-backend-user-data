    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """Return False - path and excluded_paths will be used later
        now, you don’t need to take care of them.
        """
        if path and excluded_paths and (path in excluded_paths or
                                        (path + "/") in excluded_paths):
            return False
        return True
