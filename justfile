default:
    just --list

run:
    python3 app.py

install:
    python3 -m venv venv && venv/bin/pip install -r requirements.txt && pip freeze

nuke:
    rm -rf venv/ && rm -rf src/__pycache__/
