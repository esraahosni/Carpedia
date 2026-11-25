#!/bin/bash
set -e
python3 -m pip install -r requirements.txt
python3 manage.py collectstatic --noinput
# Apply migrations only when a real database is configured
if [ -n "$DATABASE_URL" ]; then python3 manage.py migrate --noinput; fi
