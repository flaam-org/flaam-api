.PHONY: test
.DEFAULT_GOAL := help

SHELL := /bin/bash
PROJECT_NAME := flaam_api
SETTINGS := $(PROJECT_NAME).settings

help: ## Display callable targets.
	@egrep -h '\s##\s' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-15s\033[0m %s\n", $$1, $$2}'

check-venv:
	@python -c "import venv" || { echo "install python-venv"; exit 1; }

check-direnv:
	@which direnv > /dev/null || { echo "check this out https://direnv.net/#basic-installation"; exit 1; }

update: ## Install (and update) pip requirements
	@.venv/bin/pip install -U -r requirements-dev.txt

clean: ## Clean up.
	@echo "--> Removing venv"
	@rm -rf .venv
	@echo "--> Cleaning pycache files"
	@find . -type f -name '*.py[co]' -delete -o -type d -name __pycache__ -delete

init: check-venv check-direnv ## Setup Dev environment.
	@echo "--> Initializing"
	@python -m venv .venv
	@yes n | cp -vipr sample.envrc .envrc
	@direnv allow
	@make update

migration: ## Create migrations.
	@echo "--> Creating migrations"
	@python manage.py makemigrations

migrate: ## Migrate database.
	@echo "--> Migrating database"
	@python manage.py migrate

dump: ## Dump database.
	@echo "--> Dumping database"
	@python manage.py dumpdata > db_dump_$(shell date +%FT%T.%3N%Z).json

clean-db: dump ## Clear database.
	@echo "--> Dropping database"
	@python manage.py dropdb

loaddata: ## Load data from most recent db dump
	@echo "--> Loading data from db dump"
	@python manage.py loaddata $(shell ls -t db_dump_*.json | head -n 1) || { echo "Failed to load data"; exit 1; }

init-db: ## Create database.
	@echo "--> Creating database"
	@python manage.py createdb
	@make migration migrate loaddata

reinit-db: clean-db init-db ## Re-initialize database.

reinit: clean init reinit-db ## Re-initialize Dev environment.

superuser: ## Create superuser.
	@echo "--> Creating superuser"
	@python manage.py createsuperuser

run: ## Runserver.
	@python manage.py runserver

ngrok: ## Run ngrok.
	@echo "--> Starting server"
	@python manage.py runserver --noreload 0.0.0.0:8001 &
	@echo "--> Starting ngrok"
	@ngrok http 8001 --region=in &

kill-ngrok: ## Kill ngrok.
	#kill runserver
	@echo "--> Killing server"
	@kill $(shell ps aux | grep 'runserver.*8001' | grep -v grep | awk '{print $2}')
	@echo "--> Killing ngrok"
	@kill -9 $(shell ps aux | grep ngrok | grep -v grep | awk '{print $2}')
	@echo "RIP"

shell: ## Start django interactive shell.
	@python manage.py shell

db-shell: ## Access db shell.
	@python manage.py dbshell

test: ## Run tests.
	@python manage.py test

format: ## Format code.
	@echo "--> Formatting code"
	@isort . --quiet
	@black . --quiet
	@echo "All clear!"

freeze: ## Freeze dependencies.
	$(eval DEV_DEPS := $(shell cat requirements-dev.txt | tr '\n' '\|'))
	@pipdeptree -f 2>/dev/null | grep -v '^ ' | grep -vE '(${DEV_DEPS})' | tee requirements.txt

deploy: ## Deploy to production.
	@git push heroku main
	@echo "Now look for bugs!"
