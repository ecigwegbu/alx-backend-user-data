#!/usr/bin/env python3
"""
    Main file - functions that manage PII.

    Classes:
        RedactionFormatter(logging.Formatter)
    methods:
        filter_datum(fields: List[str], redaction: str,
                     message: str, separator: str) -> str:
    """

import logging
import re
from typing import List, Union


class RedactingFormatter(logging.Formatter):
    """ Redacting Formatter class
        """

    REDACTION = "***"
    FORMAT = "[HOLBERTON] %(name)s %(levelname)s %(asctime)-15s: %(message)s"
    SEPARATOR = ";"

    def __init__(self):
        """Define the object using the provided arguments"""

        super(RedactingFormatter, self).__init__(self.FORMAT)

    def format(self, record: logging.LogRecord) -> str:
        """Format the message and return a formatted version"""
        NotImplementedError


def filter_datum(fields: List[str], redaction: str,
                 message: str, separator: str) -> Union[str, None]:
    """Return an obfuscated log message."""
    for field in fields:
        ouTx: str = "{}{}=[^;]*{}".format(separator, field, separator)
        inTx: str = "{}{}={}{}".format(separator, field, redaction, separator)
        message = re.sub(ouTx, inTx, message)
    return message
