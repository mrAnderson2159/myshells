# myshells

Personal collection of shell utilities, CLI tools, experiments, automations, and random terminal-based programs developed over the years.

This repository is not a single application: it is a monorepo-style toolbox containing many independent utilities written mainly in Python, JavaScript, C, and shell scripts.

## Philosophy

`myshells` was born as a personal command-line ecosystem.

Most tools solve real problems encountered during daily usage of Linux/macOS/Windows terminals, automation workflows, file management, personal organization, gaming utilities, scripting, or experimentation.

The repository intentionally keeps a "toolbox" structure rather than forcing everything into a single rigid architecture.

---

# Environment Management

The project uses:

- `uv` for virtual environment and dependency management
- `setuptools` for packaging and script installation

The repository contains a single shared virtual environment at the project root.

This means:

- one `.venv`
- one `pyproject.toml`
- one package namespace (`myshells`)
- many independent command-line tools

The goal is simplicity and centralized dependency management.

---

# Installation

## Clone the repository

```bash
git clone git@github.com:mrAnderson2159/myshells.git
cd myshells
```

---

## Create the virtual environment

```bash
uv sync
```

This creates:

```text
.venv/
```

and installs the project in editable mode inside the environment.

---

## Activate the environment

Linux/macOS:

```bash
source .venv/bin/activate
```

Windows PowerShell:

```powershell
.venv\Scripts\Activate.ps1
```

---

# Installing CLI Commands

To make commands globally available:

```bash
uv tool install -e .
```

This installs all scripts defined in:

```toml
[project.scripts]
```

Example:

```toml
[project.scripts]
xcat = "myshells.xcat:main"
hcln = "myshells.history_cleaner.cli:main"
```

After installation, commands like:

```bash
xcat
hcln
```

can be executed directly from the terminal.

---

# Why setuptools instead of uv_build?

The project currently uses:

```toml
[build-system]
requires = ["setuptools>=61"]
build-backend = "setuptools.build_meta"
```

instead of `uv_build`.

Reason:

- the repository has a partially "flat" historical structure
- many tools were created long before modern Python packaging conventions
- `setuptools` handles this layout more reliably without forcing a major refactor

`uv` is still fully used for:

- dependency management
- virtual environments
- lockfiles
- editable installations
- tool installations

---

# Repository Structure

The repository contains:

- standalone Python utilities
- JavaScript scripts
- experimental projects
- CLI tools
- automation scripts
- small databases
- gaming-related utilities
- terminal productivity tools
- historical code and prototypes

Some directories are fully structured mini-projects, while others are single-file utilities.

This mixed structure is intentional.

---

# Development Notes

## Install the project in editable mode

```bash
pip install -e .
```

or:

```bash
uv pip install -e .
```

Editable installation allows immediate testing of local code changes without reinstalling the package.

---

## Add dependencies

Example:

```bash
uv add rich
```

This updates:

- `pyproject.toml`
- `uv.lock`

---

## Run commands during development

```bash
uv run xcat .
```

or after activation:

```bash
xcat .
```

---

# Important Note

This repository is heavily experimental and reflects many years of evolving coding style, ideas, and approaches.

Not every tool follows the same standards, architecture, or conventions.

That is part of the project's history and identity.
