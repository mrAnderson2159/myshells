"""Command-line interface definition for xcat.

This module owns argument parsing only.

It defines the public CLI contract: positional arguments, flags, presets,
output options, and future user-facing switches.

It should not scan files, read file contents, or apply ignore logic.
"""

import argparse
import logging
from pathlib import Path

from myshells.xcat.src.core.types import ParsedArgs
from myshells.xcat.src.ignore_presets import PRESETS

logger = logging.getLogger(__name__)


def parse_args() -> ParsedArgs:
    """Parse command-line arguments.

    Returns:
        Parsed command-line arguments.
    """
    parser = argparse.ArgumentParser(
        prog="xcat",
        description="Concatenate files under a path into a structured text stream.",
    )

    parser.add_argument(
        "paths",
        nargs="+",
        type=Path,
        help="Files or directories to scan.",
    )

    parser.add_argument(
        "-I",
        "--ignore",
        action="append",
        default=[],
        help="Ignore pattern. Can be repeated.",
    )

    parser.add_argument(
        "-o",
        "--output",
        type=Path,
        default=None,
        help="Write output to a file instead of stdout.",
    )

    parser.add_argument(
        "-a",
        "--all",
        "--ignore-all",
        dest="all",
        action="store_true",
        help="Apply all available ignore presets.",
    )

    parser.add_argument(
        "--gitignore",
        nargs="?",
        const=True,
        default=None,
        metavar="PATH",
        help="Apply patterns from .gitignore. Optionally pass a custom ignore file.",
    )

    parser.add_argument(
        "-f",
        "--force",
        action="store_true",
        help="Overwrite output file if it already exists.",
    )

    for preset_name, preset_patterns in PRESETS.items():
        if preset_name == "all":
            continue

        parser.add_argument(
            f"--{preset_name}",
            action="store_true",
            help=(
                f"Apply the {preset_name} ignore preset. "
                f"This preset will ignore: {', '.join(sorted(preset_patterns))}."
            ),
        )

    args = parser.parse_args()

    logger.debug("Parsed CLI arguments: %s", args)

    return args
