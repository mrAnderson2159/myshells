"""Output formatting utilities for xcat.

This module defines how file boundaries and content are rendered.

It owns the textual format consumed by humans, files, clipboards, and LLMs.
Changes here affect the shape of xcat's generated output.
"""

from pathlib import Path


def format_display_path(path: Path, display_root: Path | None = None) -> str:
    """Format the path shown in the file header.

    Args:
        path: Path of the file being rendered.
        display_root: Optional common root used to make the path relative.

    Returns:
        Display path as a POSIX-style string.
    """
    path = path.resolve()

    if display_root is None:
        return path.as_posix()

    display_root = display_root.resolve()

    try:
        return path.relative_to(display_root).as_posix()
    except ValueError:
        return path.as_posix()


def format_header(path: Path, display_root: Path | None = None) -> str:
    """Format the header used to mark the beginning of a file.

    Args:
        path: Path of the file being rendered.
        display_root: Optional common root used to make the path relative.

    Returns:
        The formatted file header.
    """
    display_path = format_display_path(path, display_root)

    return f"\n\n----------> {display_path} <----------\n\n"


def format_file(
    path: Path,
    content: str,
    display_root: Path | None = None,
) -> str:
    """Format a complete file block.

    Args:
        path: Path of the file being rendered.
        content: Text content of the file.
        display_root: Optional common root used to make the path relative.

    Returns:
        The formatted file block, including header and content.
    """
    return f"{format_header(path, display_root)}{content}"
