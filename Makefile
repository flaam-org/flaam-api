.PHONY: test static
.DEFAULT_GOAL := help

PROJECT_NAME := flaam_api
SETTINGS := $(PROJECT_NAME).settings

help: ## Display callable targets.
	@egrep -h '\s##\s' $(MAKEFILE_LIST) | sort | \
	awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-15s\033[0m %s\n", $$1, $$2}'

require-%:
	@command -v $(@:require-%=%) > /dev/null || { echo "$(@:require-%=%) not found in path"; exit 1; }

update: ## Install and update dependencies.
	@echo "--> Updating dependencies"
	@pipenv update

clean: ## Clean up.
	@echo "--> Removing venv"
	@pipenv --rm
	@echo "--> Cleaning pycache files"
	@find . -type f -name '*.py[co]' -delete -o -type d -name __pycache__ -delete

init: require-pipenv require-pre-commit require-direnv ## Setup Dev environment.
	@echo "--> Initializing"
	@pipenv install
	@echo "--> Copying .envrc"
	@yes n | cp -vipr sample.envrc .envrc
	@${EDITOR} .envrc
	@direnv allow
	@@echo "--> Creating database"
	@${MAKE} migrations migrate

migrations: ## Create migrations.
	@echo "--> Creating migrations"
	@pipenv run ./manage.py makemigrations

rm-migrations: ## Delete all migration files in migrations folders.
	@echo "--> Removing migrations"
	@find . -type f -path '**/migrations/**' -name '*.py' ! -name "__init__.py" -exec rm -f {} \;

migrate: ## Migrate database.
	@echo "--> Migrating database"
	@pipenv run ./manage.py migrate

dump dumpdata: ## Dump database.
	@echo "--> Dumping database"
	@pipenv run ./manage.py dumpdata tags accounts ideas implementations discussions > db_dump_$(shell date +%FT%T.%3N%Z).json

clean-db: dump ## Clear database.
	@echo "--> Dropping database"
	@pipenv run ./manage.py sqlflush | pipenv run ./manage.py dbshell

loaddata: ## Load data from most recent db dump
	@echo "--> Loading data from db dump"
	@pipenv run ./manage.py loaddata $(shell ls -t db_dump_*.json | head -n 1) || \
	{ echo "Failed to load data"; exit 1; }

init-db: ## Create database.
	@echo "--> Creating database"
	@${MAKE} migrations migrate loaddata

reinit-db: clean-db init-db ## Re-initialize database.

reinit: clean init reinit-db ## Re-initialize Dev environment.

su: ## Create superuser.
	@echo "--> Creating superuser"
	@pipenv run ./manage.py createsuperuser

r run: ## Runserver.
	@pipenv run ./manage.py runserver

ngrok: require-ngrok require-jq ## Run debugserver and ngrok.
	@echo "--> Starting server"
	@pipenv run ./manage.py runserver --noreload 0.0.0.0:8001 > /dev/null 2>&1 &
	@echo "--> Starting ngrok"
	@ngrok http 8001 --region=in --log=stdout > /dev/null 2>&1 &
	@sleep 2
	@curl -s http://127.0.0.1:4040/api/tunnels | jq '.tunnels[0].public_url' -r

kill-ngrok: ## Kill debugserver and ngrok.
	@echo "--> Killing server"
	@kill -15 $(shell ps a | awk '/[r]unserver.*8001/{print $$1}') > /dev/null 2>&1 || { echo "server not running";}
	@echo "--> Killing ngrok"
	@kill -15 $(shell ps a | awk '/[n]grok.*8001/{print $$1}') > /dev/null 2>&1 || { echo "ngrok not running";}
	@echo "RIP"

shell: ## Start django interactive shell.
	@pipenv run ./manage.py shell

db-shell: ## Access db shell.
	@pipenv run ./manage.py dbshell

test: ## Run tests.
	@pipenv run ./manage.py test

lint: ## Lint code.
	@echo "--> Formatting code"
	@pre-commit run --all-files
	@echo "All clear!"

deploy: ## Deploy to production.
	@git push heroku main
	@echo "Now look for bugs!"

static: ## Collect static files.
	@echo "--> Collecting static files"
	@pipenv run ./manage.py collectstatic --noinput
