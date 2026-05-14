"""Runtime resolution utilities for xcat.

This module converts parsed CLI arguments into concrete runtime values.

It resolves the scan root, combines ignore presets, applies explicit ignore
patterns, and optionally loads patterns from a gitignore-style file.

It should not parse command-line arguments, scan files, or write output.
"""

import argparse
import logging
from pathlib import Path

from myshells.xcat.src.core.types import IgnorePatternSet
from myshells.xcat.src.ignore_presets import PRESETS

logger = logging.getLogger(__name__)


def resolve_root(path: Path) -> Path:
    """Resolve and validate the scan root.

    Args:
        path: File or directory path received from the CLI.

    Returns:
        Absolute resolved path.

    Raises:
        FileNotFoundError: If the path does not exist.
    """
    root = path.resolve()

    if not root.exists():
        raise FileNotFoundError(f"path not found: {root}")

    return root


def resolve_gitignore_path(
    root: Path, gitignore_arg: str | bool | None
) -> Path | None:
    """Resolve the gitignore file path requested by the user.

    Args:
        root: Resolved scan root.
        gitignore_arg: Value of the ``--gitignore`` CLI argument.

    Returns:
        Resolved gitignore path, or None if gitignore support was not requested.
    """
    if gitignore_arg is None or gitignore_arg is False:
        return None

    if gitignore_arg is True:
        base_dir = root.parent if root.is_file() else root
        return base_dir / ".gitignore"

    gitignore_path = Path(gitignore_arg)

    if gitignore_path.is_absolute():
        return gitignore_path.resolve()

    base_dir = root.parent if root.is_file() else root
    return (base_dir / gitignore_path).resolve()


def load_ignore_file(path: Path) -> IgnorePatternSet:
    """Load ignore patterns from a gitignore-style file.

    Args:
        path: Ignore file path.

    Returns:
        Set of loaded ignore patterns.

    Notes:
        This is not full gitignore semantics yet. Empty lines, comments, and
        negation rules are skipped.
    """
    if not path.exists():
        logger.debug("Ignore file not found: %s", path)
        return set()

    patterns: IgnorePatternSet = set()

    for line in path.read_text(encoding="utf-8", errors="ignore").splitlines():
        normalized = line.strip()

        if not normalized:
            continue

        if normalized.startswith("#"):
            continue

        if normalized.startswith("!"):
            logger.debug(
                "Skipping unsupported gitignore negation: %s", normalized
            )
            continue

        patterns.add(normalized)

    logger.debug("Loaded %d patterns from ignore file: %s", len(patterns), path)

    return patterns


def resolve_ignore_patterns(
    args: argparse.Namespace, root: Path
) -> IgnorePatternSet:
    """Resolve all ignore patterns requested by the user.

    Args:
        args: Parsed CLI arguments.
        root: Resolved scan root.

    Returns:
        Combined ignore pattern set.
    """
    patterns: IgnorePatternSet = set()

    for preset_name, preset_patterns in PRESETS.items():
        if getattr(args, preset_name, False):
            logger.debug("Applying ignore preset: %s", preset_name)
            patterns |= preset_patterns

    patterns.update(args.ignore)

    gitignore_path = resolve_gitignore_path(root, args.gitignore)

    if gitignore_path is not None:
        patterns |= load_ignore_file(gitignore_path)

    logger.debug("Resolved %d ignore patterns", len(patterns))

    return patterns
