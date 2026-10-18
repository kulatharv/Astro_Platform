import logging
import sys

from .config import settings


def configure_logging() -> None:
    """Configure system-wide application logging format and level."""
    level = logging.DEBUG if settings.debug else logging.INFO
    logging.basicConfig(
        level=level,
        format="%(asctime)s [%(levelname)s] [%(name)s]: %(message)s",
        handlers=[logging.StreamHandler(sys.stdout)],
        force=True,
    )


def get_logger(name: str) -> logging.Logger:
    """Retrieve a configured logger for the specified module name."""
    configure_logging()
    return logging.getLogger(name)
