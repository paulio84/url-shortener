# Load .env file if it exists
ifneq (,$(wildcard .env))
	include .env
	export
endif

.PHONY: run test migrate upgrade downgrade shell docker-build docker-up docker-down docker-up-build docker-dev-up docker-dev-down

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
docker-build:
	docker compose build

docker-up:
	docker compose up

docker-down: 
	docker compose down

docker-up-build:
	docker compose up --build

docker-dev-up:
	docker compose -f docker-compose.dev.yml up -d

docker-dev-down:
	docker compose -f docker-compose.dev.yml down
