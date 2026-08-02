#!/usr/bin/env bash
# Provisions the dev environment. Idempotent: safe to re-run on container rebuild.
set -euo pipefail

if ! command -v uv >/dev/null 2>&1; then
    curl -LsSf https://astral.sh/uv/install.sh | sh
fi
export PATH="$HOME/.local/bin:$PATH"

# Create .venv from uv.lock, including the `dev` dependency group.
uv sync

# Install the prek git hooks (pre-commit + commit-msg for commitizen).
uv run prek install --hook-type pre-commit --hook-type commit-msg
