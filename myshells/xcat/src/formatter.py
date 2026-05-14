"""Output formatting utilities for xcat.

This module defines how file boundaries and content are rendered.

It owns the textual format consumed by humans, files, clipboards, and LLMs.
Changes here affect the shape of xcat's generated output.
"""

from pathlib import Path


def format_header(path: Path) -> str:
    """Format the header used to mark the beginning of a file.

    Args:
        path: Path of the file being rendered.

    Returns:
        The formatted file header.
    """
    return f"\n\n----------> {path} <----------\n\n"


def format_file(path: Path, content: str) -> str:
    """Format a complete file block.

    Args:
        path: Path of the file being rendered.
        content: Text content of the file.

    Returns:
        The formatted file block, including header and content.
    """
    return f"{format_header(path)}{content}"
