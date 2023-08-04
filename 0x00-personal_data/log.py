#!/usr/bin/env python3

import logging

logger = logging.getLogger(__name__)
logging.basicConfig(filename="log.txt", level=logging.DEBUG)

logger.info("Hello, World!")
logger.debug("Hello, World Again!")
print(dir(logger))

