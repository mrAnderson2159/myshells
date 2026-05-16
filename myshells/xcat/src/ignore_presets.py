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

CSHARP = BASE | {
    # Build outputs
    "bin",
    "obj",
    # Project / Solution metadata
    "*.resx",
    "*.datasource",
    "*.csproj",
    "*.log",
    # Visual Studio / Rider
    ".vs",
    ".idea",
    "*.suo",
    "*.user",
    "*.userosscache",
    "*.sln.docstates",
    "*.rsuser",
    # NuGet / packages
    "packages",
    "*.nupkg",
    # Test / coverage
    "TestResults",
    "coverage",
    "coverage.xml",
    "coverage.json",
}

ALL = PYTHON | REACT | CSHARP

PRESETS = {
    "base": BASE,
    "python": PYTHON,
    "node": NODE,
    "react": REACT,
    "csharp": CSHARP,
    "all": ALL,
}
