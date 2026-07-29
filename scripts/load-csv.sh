#!/bin/bash -ex

ROOT_DIR="$(cd "$(dirname "$0")/.." && pwd)"
cd "$ROOT_DIR"

source .venv/bin/activate
python3 scripts/load_csv.py
