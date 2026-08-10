#!/bin/bash -ex
source .venv/bin/activate
export FLASK_DEBUG="${FLASK_DEBUG:-1}"
python3 main.py
