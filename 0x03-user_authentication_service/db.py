#!/usr/bin/env python3
"""DB module. This module enables access to the database of the app.
"""
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.session import Session
from sqlalchemy.exc import InvalidRequestError
from sqlalchemy.orm.exc import NoResultFound
from user import Base, User


class DB:
    """DB class. This class implements the database handler methods.
       Only its public methods should be accessed from outside.
    """

    def __init__(self) -> None:
        """Initialize a new DB instance. Takes care of instance variables.
        """
        # self._engine = create_engine("sqlite:///a.db", echo=True)
        self._engine = create_engine("sqlite:///a.db")
        Base.metadata.drop_all(self._engine)
        Base.metadata.create_all(self._engine)
        self.__session = None

    @property
    def _session(self) -> Session:
        """Memoized session object. This property enables a session handle.
        """
        if self.__session is None:
            DBSession = sessionmaker(bind=self._engine)
            self.__session = DBSession()
        return self.__session

    def add_user(self, email: str, hashed_password: str) -> User:
        """Save the user to a database. Rquires no validation for now.
        """
        new_user = User(email=email, hashed_password=hashed_password)
        if self._session is None:
            return None
        self._session.add(new_user)
        self._session.commit()
        self._session.refresh(new_user)

        return new_user

    def find_user_by(self, **kwargs) -> User:
        """Based on given kwargs and filter users to retrieve the first user
        """
        try:
            user = self._session.query(User).filter_by(**kwargs).first()
            if user is None:
                raise NoResultFound
        except Exception:
            raise
        return user
