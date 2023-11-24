.PHONY: help
help: ## Show this help
	@egrep -h '\s##\s' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-20s\033[0m %s\n", $$1, $$2}'

.PHONY: docker-build
docker-build:	## Build project with compose
	docker-compose build

.PHONY: docker-up
docker-up:	## Run project with compose
	docker-compose up --remove-orphans

.PHONY: docker-clean
docker-clean: ## Clean Reset project containers and volumes with compose
	docker-compose down -v --remove-orphans | true
	docker-compose rm -f | true
	docker volume rm fastapi_postgres_data | true

.PHONY: db_migrations
docker-apply-db-migrations: ## apply alembic migrations to database/schema
	docker-compose run --rm app alembic upgrade head

.PHONY: db_update
docker-create-db-migration:  ## Create new alembic database migration aka database revision.
	docker-compose up -d db | true
	docker-compose run --no-deps app alembic revision --autogenerate -m "$(msg)"

.PHONY: docker-test
docker-test:	## Run project tests
	docker-compose -f docker-compose.yml -f docker-compose.test.yml  run --rm app pytest

.PHONY: safety
safety:	## Check project and dependencies with safety https://github.com/pyupio/safety
	docker-compose run --rm app safety check

.PHONY: py-upgrade
py-upgrade:	## Upgrade project py files with pyupgrade library for python version 3.10
	pyupgrade --py311-plus `find app -name "*.py"`

.PHONY: lint
lint:  ## Lint project code.
	poetry run ruff --fix .

.PHONY: model-generate
model-generate: ## generate sqlalchemy models from database
	poetry run sqlacodegen --generator declarative postgresql://user:secret@0.0.0.0/devdb --outfile models.py --schemas shakespeare
