"""This module provides a logging setup for the application,
allowing for both console and file logging with configurable levels and formats.
"""

import logging
from logging.handlers import TimedRotatingFileHandler
from pathlib import Path


def get_level(level_name: str) -> int:
    """Convert a logging level name (e.g., 'INFO', 'DEBUG') to its corresponding logging level integer.

    Args:
        level_name (str): The name of the logging level to convert.

    Returns:
        int: The corresponding logging level integer.
    Raises:
        ValueError: If the provided level_name is not a valid logging level.
    """
    level = getattr(logging, level_name.upper(), None)

    if not isinstance(level, int):
        raise ValueError(f"Invalid logging level: {level_name}")

    return level


def setup_logger(
    name: str,
    log_path: Path,
    level_name: str,
    datefmt: str = "%d-%m-%Y %H:%M:%S",
) -> logging.Logger:
    """
    Configure and return a named logger.
    Must be called ONCE in main.

    Args:
        name (str): The name of the logger.
        log_path (Path): The path to the log directory.
        level_name (str): The name of the logging level.
        datefmt (str, optional): The date format for log messages. Defaults to "%d-%m-%Y %H:%M:%S".

    Returns:
        logging.Logger: The configured logger.
    """

    logger = logging.getLogger(name)

    # evita duplicazioni
    if logger.handlers:
        return logger

    level = get_level(level_name)

    formatter = logging.Formatter(
        "%(asctime)s - %(name)s - %(levelname)s - %(message)s", datefmt=datefmt
    )

    logger.setLevel(level)

    # 🔹 console handler
    console_handler = logging.StreamHandler()
    console_handler.setLevel(level)
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)

    # 🔹 file handler
    log_dir = Path(log_path)
    log_dir.mkdir(parents=True, exist_ok=True)

    file_handler = TimedRotatingFileHandler(
        log_dir / "app.log",
        when="midnight",
        interval=1,
        backupCount=7,
        encoding="utf-8",
    )
    file_handler.setLevel(level)
    file_handler.setFormatter(formatter)

    logger.addHandler(file_handler)

    return logger
