#!/usr/bin/env python3
"""
    Main file - functions that manage PII.

    Classes:
        RedactionFormatter(logging.Formatter)
    Methods:
        filter_datum(fields: List[str], redaction: str,
                     message: str, separator: str) -> str:
    """

import logging
import re
from typing import List
import mysql.connector
from mysql.connector.connection import MySQLConnection
import os


PII_FIELDS = ("name", "email", "phone", "ssn", "password")
"""Personally Identifiable Information for users"""


def filter_datum(fields: List[str], redaction: str,
                 message: str, separator: str) -> str:
    """ Return an obfuscated log message.

        Keyword arguments:
        fields: List[str] -- a list of fields to obfusecate
        redaction: str -- the string to replace the fields with
        message: str -- the log message
        """

    for field in fields:
        ouTx: str = r"{}=[^{}]*".format(field, separator)
        inTx: str = "{}={}".format(field, redaction)
        message = re.sub(ouTx, inTx, message)
    return message


class RedactingFormatter(logging.Formatter):
    """ Redacting Formatter class
        """

    REDACTION = "***"
    FORMAT = "[HOLBERTON] %(name)s %(levelname)s %(asctime)-15s: %(message)s"
    SEPARATOR = ";"

    def __init__(self, fields: List[str]):
        """Define the object using the provided arguments."""

        super(RedactingFormatter, self).__init__(self.FORMAT)
        self.fields = fields

    def format(self, record: logging.LogRecord) -> str:
        """Format the message and return a formatted version."""
        obfuscated_message = filter_datum(self.fields, self.REDACTION,
                                          record.msg, self.SEPARATOR)
        record.msg = obfuscated_message
        return super().format(record)


def get_logger() -> logging.Logger:
    """Return a logging.Logger object"""

    logger = logging.getLogger("user_data")
    logger.setLevel(logging.INFO)
    logger.propagate = False
    formatter = RedactingFormatter(list(PII_FIELDS))
    stream_handler = logging.StreamHandler()
    stream_handler.setFormatter(formatter)
    logger.addHandler(stream_handler)
    return logger


def get_db() -> MySQLConnection:
    """Return a connection to a dbase based on os environmental variables"""

    host = os.getenv('PERSONAL_DATA_DB_HOST')
    db = os.getenv('PERSONAL_DATA_DB_NAME')
    username = os.getenv('PERSONAL_DATA_DB_USERNAME')
    password = os.getenv('PERSONAL_DATA_DB_PASSWORD')

    kwargs = {
        'user': username,
        'password': password,
        'host': host,
        'database': db
    }
    connector = mysql.connector.connect(**kwargs)

    return connector


if __name__ == "__main__":
    pass
