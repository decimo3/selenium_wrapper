#!/bin/env bash

set -e

if [[ -z "$VIRTUAL_ENV" ]]; then
    python -m venv .venv
    source .venv/Scripts/activate
fi

# DONE - Fetch tags and get the latest one
git fetch --tags
version=$(git describe --tags $(git rev-list --tags --max-count=1))

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
