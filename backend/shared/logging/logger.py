"""Centralized Application Logging Infrastructure."""

import sys
import logging
from shared.config import settings


def setup_logger(name: str = "app") -> logging.Logger:
    logger = logging.getLogger(name)
    log_level = logging.DEBUG if settings.DEBUG else logging.INFO
    logger.setLevel(log_level)

    if not logger.handlers:
        handler = logging.StreamHandler(sys.stdout)
        handler.setLevel(log_level)
        formatter = logging.Formatter(
            "%(asctime)s [%(levelname)s] [%(name)s]: %(message)s"
        )
        handler.setFormatter(formatter)
        logger.addHandler(handler)

    return logger


logger = setup_logger()
get_logger = setup_logger
