#!/bin/bash
set -e
# Vercel's Python is externally managed (PEP 668), so build inside a private virtualenv.
VENV=/tmp/build-venv
if command -v uv >/dev/null 2>&1; then
  uv venv "$VENV"
  uv pip install --python "$VENV/bin/python" -r requirements.txt
else
  python3 -m venv "$VENV"
  "$VENV/bin/python" -m pip install -r requirements.txt
fi
PY="$VENV/bin/python"
# collectstatic does not touch the database; a placeholder key avoids a build failure if the real one is missing
SECRET_KEY="${SECRET_KEY:-build-only-placeholder}" "$PY" manage.py collectstatic --noinput
# Apply migrations only when a real database is configured
if [ -n "$DATABASE_URL" ]; then "$PY" manage.py migrate --noinput; fi
