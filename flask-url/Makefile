.PHONY: migrate upgrade downgrade shell run test

migrate:
	uv run flask db migrate -m "$(m)"

upgrade:
	uv run flask db upgrade

downgrade:
	uv run flask db downgrade

shell:
	uv run flask shell

run:
	uv run flask run

test:
	uv run pytest -v