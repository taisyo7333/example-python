#!/bin/bash -ex

ROOT_DIR="$(cd "$(dirname "$0")/.." && pwd)"
cd "$ROOT_DIR"

# Latest stable Python (override with PYTHON_VERSION=3.13 if needed)
PYTHON_VERSION="${PYTHON_VERSION:-3.14}"

export PATH="${HOME}/.local/bin:${PATH}"

if ! command -v uv >/dev/null 2>&1; then
  curl -LsSf https://astral.sh/uv/install.sh | sh
  export PATH="${HOME}/.local/bin:${PATH}"
fi

uv python install "${PYTHON_VERSION}"
rm -rf .venv
uv venv --python "${PYTHON_VERSION}" .venv
# shellcheck disable=SC1091
source .venv/bin/activate
uv pip install -r requirements.txt
python --version
