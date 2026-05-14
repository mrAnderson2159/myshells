"""Logging setup for xcat."""

import logging
import sys


def get_level(level_name: str) -> int:
    """Convert a logging level name to its corresponding logging level integer.

    Args:
        level_name: Logging level name.

    Returns:
        Corresponding logging level integer.

    Raises:
        ValueError: If the provided level name is invalid.
    """
    level = getattr(logging, level_name.upper(), None)

    if not isinstance(level, int):
        raise ValueError(f"Invalid logging level: {level_name}")

    return level


def setup_logger(
    name: str,
    level_name: str = "WARNING",
    datefmt: str = "%d-%m-%Y %H:%M:%S",
) -> logging.Logger:
    """Configure and return a named stderr logger.

    Args:
        name: Logger name.
        level_name: Logging level name.
        datefmt: Date format for log messages.

    Returns:
        Configured logger.
    """
    logger = logging.getLogger(name)

    if logger.handlers:
        return logger

    level = get_level(level_name)

    formatter = logging.Formatter(
        "%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        datefmt=datefmt,
    )

    handler = logging.StreamHandler(sys.stderr)
    handler.setLevel(level)
    handler.setFormatter(formatter)

    logger.setLevel(level)
    logger.addHandler(handler)

    return logger
