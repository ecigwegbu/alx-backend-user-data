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
from typing import List


class RedactingFormatter(logging.Formatter):
    """ Redacting Formatter class
        """

    REDACTION = "***"
    FORMAT = "[HOLBERTON] %(name)s %(levelname)s %(asctime)-15s: %(message)s"
    SEPARATOR = ";"

    def __init__(self):
        super(RedactingFormatter, self).__init__(self.FORMAT)

    def format(self, record: logging.LogRecord) -> str:
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
        out_text: str = "{}{}=[^;]*{}".format(separator, field, separator)
        in_text: str = "{}{}={}{}".format(separator, field, redaction,
                                          separator)
        message = re.sub(out_text, in_text, message)
    return message
