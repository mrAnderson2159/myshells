"""Ignore matching utilities for xcat.

This module decides whether a file or directory should be skipped.

It is responsible for matching paths against ignore patterns, including
plain names, relative paths, glob-style patterns, and eventually richer
ignore semantics.

It should not walk directories or read file contents.
"""

from fnmatch import fnmatch
from pathlib import Path

from myshells.xcat.src.core.types import IgnorePatterns


def should_ignore(path: Path, root: Path, patterns: IgnorePatterns) -> bool:
    """Return True if path matches one of the ignore patterns.

    Args:
        path: File or directory path to test.
        root: Root directory of the scan.
        patterns: Ignore patterns to apply.

    Returns:
        True if the path should be ignored, otherwise False.
    """
    path = path.absolute()
    root = root.absolute()

    try:
        rel = path.relative_to(root).as_posix()
    except ValueError:
        return True

    name = path.name

    for pattern in patterns:
        normalized = pattern.strip().strip("/")

        if not normalized:
            continue

        if (
            fnmatch(name, normalized)
            or fnmatch(rel, normalized)
            or fnmatch(rel, f"{normalized}/**")
        ):
            return True

    return False
