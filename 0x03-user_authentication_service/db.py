"""DB module
"""
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.session import Session
from typing import Union
from user import Base, User


class DB:
    """DB class
    """

    def __init__(self) -> None:
        """Initialize a new DB instance
        """
        # self._engine = create_engine("sqlite:///a.db", echo=True)
        self._engine = create_engine("sqlite:///a.db")
        Base.metadata.drop_all(self._engine)
        Base.metadata.create_all(self._engine)
        self.__session = None

    @property
    def _session(self) -> Union[Session, None]:
        """Memoized session object
        """
        if self.__session is None:
            DBSession = sessionmaker(bind=self._engine)
            self.__session = DBSession()
        return self.__session

    def add_user(self, email: str, hashed_password: str) -> Union[User, None]:
        """Save the user to a database. Rquires no validation for now.
        """
        new_user = User(email="email", hashed_password="hashed_password")
        if self._session is None:
            return None
        self._session.add(new_user)
        self._session.commit()
        self._session.refresh(new_user)

        return new_user
