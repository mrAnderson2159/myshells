#!/bin/bash
# Script to create a new git release version from the dev branch

# Ensure repository is clean and up to date
if [ -n "$(git status --porcelain)" ]; then
  echo "Repository has uncommitted changes. Please commit or stash them before running this script."
  exit 1
fi
git fetch origin
git checkout dev && git pull --ff-only origin dev
git checkout master && git pull --ff-only origin master

# Get latest git version of the current software by checking dev branch
LATEST_VERSION=$(git describe --tags --abbrev=0 dev)

# Check if we got a version and dev branch exists
if [ -z "$LATEST_VERSION" ]; then
  # No tags found, check if dev branch exists
  if [ -n "$(git branch --list dev)" ]; then
    echo "Dev branch exists but no tags found. Starting from v0.0.0"
    LATEST_VERSION="v0.0.0"
    git tag "v0.0.0"
  else
    echo "Could not determine the latest version from the dev branch. Is dev branch available?"
    exit 1
  fi
fi

# Get new version from user input or command line argument
if [ -n "$1" ]; then
  NEW_VERSION="$1"
else
  read -p "The latest version is $LATEST_VERSION. Enter new version or press Enter to abort (e.g., v1.2.3 or 1.2.3): " NEW_VERSION
fi

# If user pressed Enter without input, abort
if [ -z "$NEW_VERSION" ]; then
  echo "Aborting version update."
  exit 0
fi

# Check version syntax
if [[ ! "$NEW_VERSION" =~ ^v?[0-9]+\.[0-9]+\.[0-9]+$ ]]; then
  echo "Invalid version format. Please use semantic versioning (e.g., v1.2.3 or 1.2.3)."
  exit 1
fi

# If version does not start with 'v', prepend it
if [[ "$NEW_VERSION" != v* ]]; then
  NEW_VERSION="v$NEW_VERSION"
fi

# Compare versions
LV_MAJOR=$(echo "$LATEST_VERSION" | sed -E 's/^v([0-9]+)\..*/\1/')
LV_MINOR=$(echo "$LATEST_VERSION" | sed -E 's/^v[0-9]+\.([0-9]+)\..*/\1/')
LV_PATCH=$(echo "$LATEST_VERSION" | sed -E 's/^v[0-9]+\.[0-9]+\.([0-9]+).*/\1/')

NV_MAJOR=$(echo "$NEW_VERSION" | sed -E 's/^v([0-9]+)\..*/\1/')
NV_MINOR=$(echo "$NEW_VERSION" | sed -E 's/^v[0-9]+\.([0-9]+)\..*/\1/')
NV_PATCH=$(echo "$NEW_VERSION" | sed -E 's/^v[0-9]+\.[0-9]+\.([0-9]+).*/\1/')

# Pad numbers for comparison
LV=$(printf "%03d%03d%03d" $LV_MAJOR $LV_MINOR $LV_PATCH)
NV=$(printf "%03d%03d%03d" $NV_MAJOR $NV_MINOR $NV_PATCH)

if [ "$NV" -le "$LV" ]; then
  echo "New version $NEW_VERSION must be greater than the latest version $LATEST_VERSION."
  exit 1
fi

# Get LEATEST_VERSION hash
LATEST_HASH=$(git rev-parse "$LATEST_VERSION")

# Execute git commands to create new version
git switch master

echo "🚀 Applying commits from dev onto master..."
if ! git cherry-pick "$LATEST_HASH"..dev --no-commit; then
  echo ""
  echo "⚠️  Cherry-pick encountered conflicts."
  echo "👉  Please open another terminal, resolve the conflicts manually (add, remove, or edit files as needed),"
  echo "    then return here and confirm when you're ready to continue."
  echo ""
  read -rp "Have you resolved all conflicts and staged the changes? (y/n): " RESOLVED
  if [[ "$RESOLVED" != "y" && "$RESOLVED" != "Y" ]]; then
    echo "❌ Aborting cherry-pick process. Reverting..."
    git cherry-pick --abort
    exit 1
  fi
fi

# Commit the result (either clean or post-merge)
echo ""
git commit -m "Release $NEW_VERSION"

# Show recent log for verification
echo ""
echo "🧾 Here's the latest commit history on master:"
git --no-pager log --oneline -n 5 | cat
echo ""

read -rp "✅ Do you want to tag dev with $NEW_VERSION and push to origin? (y/n): " CONFIRM

if [[ "$CONFIRM" != "y" && "$CONFIRM" != "Y" ]]; then
  echo "❌ Aborting. Deleting the new commit..."
  git reset --hard HEAD~1
  exit 0
fi

echo "🏷️  Tagging and pushing..."
git push && git tag "$NEW_VERSION" dev && git push --tags

echo "🎉 Done! Version $NEW_VERSION successfully released."
