# Load .env file if it exists
ifneq (,$(wildcard .env))
	include .env
	export
endif

.PHONY: run test migrate upgrade downgrade shell docker-stage-up docker-stage-down docker-dev-up docker-dev-down

# Local development
run:
	uv run flask run

test:
	uv run pytest -v

migrate:
	uv run flask db migrate -m "$(m)"

upgrade:
	uv run flask db upgrade

downgrade:
	uv run flask db downgrade

shell:
	uv run flask shell

# Docker
docker-stage-up:
	docker compose -f docker-compose.staging.yml up -d --build

docker-stage-down: 
	docker compose -f docker-compose.staging.yml down

docker-dev-up:
	docker compose -f docker-compose.dev.yml up -d

docker-dev-down:
	docker compose -f docker-compose.dev.yml down
