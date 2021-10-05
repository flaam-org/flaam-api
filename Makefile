SHELL := /bin/bash

.DEFAULT_GOAL := help

PROJECT_NAME=flaam_api
SETTINGS=$(PROJECT_NAME).settings

help: ## Display callable targets.
	@grep -E '^[a-zA-Z_-]+: ## .*' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-15s\033[0m %s\n", $$1, $$2}'

check-venv:
	@python -c "import venv" || { echo "install python-venv"; exit 1; }

check-direnv:
	@which direnv > /dev/null || { echo "check this out https://direnv.net/#basic-installation"; exit 1; }

init: check-venv check-direnv ## Setup Dev environment.
	@echo "Initializing project $(PROJECT_NAME)"
	@python -m venv .venv
	@yes n | cp -vipr sample.envrc .envrc
	@direnv allow
	@make update

run: ## Runserver.
	@python manage.py runserver

shell: ## Start django interactive shell.
	@python manage.py shell

dump: ## Dump database.
	@python manage.py dumpdb > db.json

migration: ## Create migrations.
	@python manage.py makemigrations

migrate: ## Migrate database.
	@python manage.py migrate

format: ## Format code.
	@isort $(PROJECT_NAME) --quiet
	@black $(PROJECT_NAME) --quiet
	@echo "All clear!"

freeze: ## Freeze dependencies.
	$(eval DEV_DEPS := $(shell cat requirements-dev.txt | tr '\n' '\|'))
	@pipdeptree -f 2>/dev/null | grep -v '^ ' | grep -vE '(${DEV_DEPS})' | tee requirements.txt

deploy: ## Deploy to production.
	@git push heroku main

update: ## Install (and update) pip requirements
	@.venv/bin/pip install -U -r requirements-dev.txt
