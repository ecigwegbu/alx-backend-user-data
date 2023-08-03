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


class RedactingFormatter(logging.Formatter):
    """ Redacting Formatter class
        """

    REDACTION = "***"
    FORMAT = "[HOLBERTON] %(name)s %(levelname)s %(asctime)-15s: %(message)s"
    SEPARATOR = ";"

    def __init__(self):
        """Init the object."""
        super(RedactingFormatter, self).__init__(self.FORMAT)

    def format(self, record: logging.LogRecord) -> str:
        """Define this method."""
        NotImplementedError


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


if __name__ == "__main__":
    pass
