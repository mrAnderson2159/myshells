# !/bin/bash
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
LATEST_VERSION=$(git describe --tags $(git rev-list -n 1 dev))

# Check if we got a version and dev branch exists
if [ -z "$LATEST_VERSION" ]; then
  # No tags found, check if dev branch exists
  if [ -n "$(git branch --list dev)" ]; then
    echo "Dev branch exists but no tags found. Starting from v1.0.0"
    LATEST_VERSION="v1.0.0"
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
git cherry-pick "$LATEST_HASH"^..dev --no-commit
git commit

# Check if user is satisfied with the commit
git log --oneline master | cat

read -p "If you are satisfied with the commit, I will now tag dev with $NEW_VERSION and push to origin. Else I will delete the commit. Proceed? (y/n): " CONFIRM

if [[ "$CONFIRM" != "y" ]]; then
  echo "Aborting. Deleting the commit."
  git reset --hard HEAD~1
  exit 0
fi


git push && git tag "$NEW_VERSION" dev && git push --tags
