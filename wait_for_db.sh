#!/bin/sh
set -e

echo "Waiting for postgres..."
until nc -z db 5432; do
  sleep 1
done

echo "Postgres is up - executing command"
exec "$@"
