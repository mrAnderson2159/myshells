# Versioning Workflow

This document describes the recommended versioning workflow for software projects.

---

## General Principles

-   There are two main branches:

    -   **`dev`**: continuous development line, contains _all_ granular commits.
    -   **`master`**: release line, contains only consolidated commits obtained via cherry-pick.

-   **Version tags** (`vX.Y.Z`) exist exclusively on `dev`.
    Each tag points to the last commit included in a release.

-   The `master` branch has no tags, but each of its commits logically corresponds to a tag present on `dev`.

---

## Graphical Example

### Dev branch

```
A (tag: v1.1.0) -- B -- C (tag: v1.1.5) -- D (tag: v1.2.0) -- E -- F
```

### Master branch

```
v1.1.0 -- v1.1. -- v1.2.0
```

---

## Release Process

1. **Development on `dev`**

    - New features and fixes are added to `dev`.
    - When a release is decided, the latest tag on `dev` (`LATEST_VERSION`) is identified.

2. **Creating a New Version**

    - Run the `new_git_version.sh` script.
    - The script:
        - calculates the new version (`NEW_VERSION`),
        - cherry-picks from `LATEST_VERSION` up to `dev` onto `master`,
        - creates a new consolidated commit on `master`.

3. **Tagging**
    - A new tag is created on `dev`, pointing to the last commit included in the release.
    - `master` remains without tags, but its latest commit semantically corresponds to that tag.

---

## Model Advantages

-   **Clarity**: `master` shows only the sequence of releases, without noise.
-   **Traceability**: tags on `dev` allow you to trace exactly which commits are included.
-   **Flexibility**: you can freely develop on `dev` without "polluting" `master`.

---

## Useful Commands

-   Check the latest tag on `dev`:
    ```bash
    git describe --tags dev
    ```
-   Get the hash of a tag:
    ```bash
    git rev-parse vX.Y.Z
    ```
-   Create a release:
    ```bash
    ./new_git_version.sh
    ```

---
