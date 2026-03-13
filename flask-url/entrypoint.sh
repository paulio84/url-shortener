#!/bin/sh
set -e

echo "Starting in '${FLASK_ENV}' environment..."
echo "Running database migrations..."
flask db upgrade

echo "Starting application..."
exec "$@"