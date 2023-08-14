#!/usr/bin/env python3
"""Create an SQLAlchemy table user using ORM and mapping declaration
"""
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker


Base = declarative_base()


class User(Base):
    """Create a model User with given attributes
    """
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    email = Column(String(250), nullable=False)
    hashed_password = Column(String(250), nullable=False)
    session_id = Column(String(250), nullable=True)
    reset_token = Column(String(250), nullable=True)
