"""Built-in ignore presets for xcat.

This module defines reusable sets of ignore patterns.

Presets are composed with normal Python set operations, so specialized
presets can build on more general ones, for example:

    PYTHON = BASE | {...}
    REACT = NODE | {...}

The CLI may expose these presets as flags such as ``--python`` or
``--react``.
"""

BASE = {
    # Git / environments
    ".git",
    ".venv",
    # Python cache/build
    "__pycache__",
    "*.pyc",
    "*.pyo",
    "*.egg-info",
    # Editors / IDEs
    ".idea",
    ".vscode",
    # macOS
    ".DS_Store",
    "._*",
    # Windows
    "Thumbs.db",
    "desktop.ini",
    # Linux / generic temp files
    "*~",
    "*.swp",
    ".swp",
}

PYTHON = BASE | {
    ".pytest_cache",
    ".mypy_cache",
    ".ruff_cache",
    "dist",
    "build",
    "htmlcov",
    ".coverage",
}

NODE = BASE | {
    "node_modules",
    "dist",
    "build",
    "coverage",
}

REACT = NODE | {
    ".vite",
    ".next",
}

ALL = PYTHON | REACT

PRESETS = {
    "base": BASE,
    "python": PYTHON,
    "node": NODE,
    "react": REACT,
    "all": ALL,
}
