"""Filesystem scanning and file reading for xcat.

This module walks directories, prunes ignored folders, reads accepted files,
and returns normalized output chunks.

It delegates ignore decisions to ``matcher`` and output formatting to
``formatter``.
"""

import logging
import os
from pathlib import Path

from myshells.xcat.src.core.types import IgnorePatternSet
from myshells.xcat.src.formatter import format_file
from myshells.xcat.src.matcher import should_ignore

logger = logging.getLogger("xcat.scanner")


def read_file(path: Path) -> str:
    """Read and return the content of a file.

    Args:
        path: File path to read.

    Returns:
        The file content decoded as UTF-8.
    """
    return path.read_text(encoding="utf-8", errors="ignore")


def scan_file(path: Path) -> str:
    """Read and format a single file.

    Args:
        path: File path to scan.

    Returns:
        The formatted file block.
    """
    return format_file(path, read_file(path))


def scan_directory(root: Path, patterns: IgnorePatternSet) -> str:
    """Scan a directory recursively and concatenate accepted files.

    Args:
        root: Directory path to scan.
        patterns: Ignore patterns to apply.

    Returns:
        Concatenated formatted file blocks.
    """
    output_chunks: list[str] = []

    for current_root, dirs, files in os.walk(root):
        current_path = Path(current_root).resolve()

        dirs[:] = [
            directory
            for directory in dirs
            if not should_ignore(current_path / directory, root, patterns)
        ]

        for file in files:
            file_path = (current_path / file).resolve()

            if should_ignore(file_path, root, patterns):
                continue

            try:
                output_chunks.append(scan_file(file_path))
            except Exception as exc:
                logger.warning("Could not read file: %s (%s)", file_path, exc)

    return "".join(output_chunks)


def scan_path(root: Path, patterns: IgnorePatternSet) -> str:
    """Scan a path and concatenate accepted files.

    Args:
        root: File or directory path to scan.
        patterns: Ignore patterns to apply.

    Returns:
        Concatenated formatted output.
    """
    root = root.resolve()

    if root.is_file():
        return scan_file(root)

    return scan_directory(root, patterns)
