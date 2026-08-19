#!/bin/env bash

set -e

if [[ -z "$VIRTUAL_ENV" ]]; then
    python -m venv .venv
    source .venv/Scripts/activate
fi

# DONE - Fetch tags and get the latest one
git fetch --tags
version=$(git describe --tags $(git rev-list --tags --max-count=1))
version_number="${version#v}"  # Remove 'v' prefix if the tag has it
echo "Version: $version_number"

# Extract major, minor, and patch versions
IFS='.' read -r MAJOR_VERSION MINOR_VERSION PATCH_VERSION <<< "$version_number"
export MAJOR_VERSION MINOR_VERSION PATCH_VERSION
echo "Major version: $MAJOR_VERSION"
echo "Minor version: $MINOR_VERSION"
echo "Patch version: $PATCH_VERSION"

# Write package descriptor file
sed -i "s/0.0.0/${MAJOR_VERSION}.${MINOR_VERSION}.${PATCH_VERSION}/g" pyproject.toml

# Install dependencies
pip install -e ".[test]"

# Lint with pylint
pylint src

# Test with pytest
pytest

# Build a package
python -m build

# Create a release on GitHub
gh release create $version --verify-tag \
    --title "${version} ($(date +%Y-%m-%d))" \
    --notes-file release_notes.md \
    "dist/*"

# Reverting placeholder files
git restore pyproject.toml
