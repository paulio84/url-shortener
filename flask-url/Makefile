.PHONY: migrate upgrade downgrade shell

migrate:
	uv run flask db migrate -m "$(m)"

upgrade:
	uv run flask db upgrade

downgrade:
	uv run flask db downgrade

shell:
	uv run flask shell