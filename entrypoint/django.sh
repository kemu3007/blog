#!/bin/sh

python3 /app/src/manage.py collectstatic --noinput
python3 /app/src/manage.py migrate

exec "$@"