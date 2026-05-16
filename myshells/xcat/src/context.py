"""Context building utilities for xcat.

This module coordinates resolved scan roots, ignore pattern resolution,
filesystem scanning, and final text aggregation.

It owns the high-level operation of turning one or more roots into a single
structured context stream.
"""

import argparse
from pathlib import Path

from myshells.xcat.src.core.types import ExcludedPaths
from myshells.xcat.src.resolver import resolve_ignore_patterns
from myshells.xcat.src.scanner import scan_path


def build_context(
    roots: list[Path],
    args: argparse.Namespace,
    excluded_paths: ExcludedPaths | None = None,
    display_root: Path | None = None,
) -> str:
    """Build a structured text context from one or more scan roots.

    Args:
        roots: Resolved file or directory roots to scan.
        args: Parsed CLI arguments used to resolve ignore behavior.
        excluded_paths: Resolved file paths that must not be scanned.
        display_root: Common display root for rendered file headers.
    Returns:
        Concatenated structured text generated from all roots.
    """
    output_chunks: list[str] = []
    excluded_paths = excluded_paths or set()

    for root in roots:
        ignore_patterns = resolve_ignore_patterns(args, root)
        output_chunks.append(
            scan_path(root, ignore_patterns, excluded_paths, display_root)
        )

    return "".join(output_chunks)
