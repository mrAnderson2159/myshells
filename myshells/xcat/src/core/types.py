"""Shared type aliases for the application."""

import argparse
from collections.abc import Iterable
from pathlib import Path

type ExcludedPaths = set[Path]
"""Concrete set of resolved filesystem paths that must not be scanned."""

type IgnorePattern = str
"""Single ignore rule used by xcat matching logic."""

type IgnorePatterns = Iterable[IgnorePattern]
"""Generic iterable collection of ignore patterns."""

type IgnorePatternSet = set[IgnorePattern]
"""Concrete mutable set of ignore patterns."""

type ParsedArgs = argparse.Namespace
"""Parsed command-line arguments."""

type PathLike = str | Path
"""Filesystem path accepted by xcat APIs."""
