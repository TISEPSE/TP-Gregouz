SHELL := bash
.ONESHELL:
.SHELLFLAGS := -eu -o pipefail -c
.DELETE_ON_ERROR:
MAKEFLAGS += --warn-undefined-variables
MAKEFLAGS += --no-builtin-rules

.PHONY: all
all:
	@echo "Commandes disponibles : run, install, nuke"

.PHONY: run
run:
	python3 app.py

.PHONY: install
install:
	python3 -m venv venv && venv/bin/pip install -r requirements.txt

.PHONY: nuke
nuke:
	rm -rf venv/ && rm -rf src/__pycache__/
