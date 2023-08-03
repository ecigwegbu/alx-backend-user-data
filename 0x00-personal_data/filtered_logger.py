#!/usr/bin/env python3
""" Main file - functions that manage PII."""
import logging
import re
from typing import List


def filter_datum(fields: List[str], redaction: str,
                 message: str, separator: str) -> str:
    """Return an obfuscated log message."""
    for field in fields:
        ouTx: str = "{}=[^{}]*".format(field, separator)
        inTx: str = "{}={}".format(field, redaction)
        message = re.sub(ouTx, inTx, message)
    return message
