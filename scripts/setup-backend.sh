#!/usr/bin/env bash
# One-time (and safe to re-run) backend setup: venv, dependencies, .env key, DB, seed data.
set -euo pipefail
cd "$(dirname "$0")/../backend"

PYTHON="${PYTHON:-$(command -v python3.12 || command -v python3)}"
echo "Using $($PYTHON --version)"

[ -d .venv ] || "$PYTHON" -m venv .venv
.venv/bin/pip install --quiet --upgrade pip
.venv/bin/pip install --quiet -e ".[dev]"

if [ ! -f .env ]; then
	umask 077
	printf 'FR_ENVIRONMENT=development\nFR_ENCRYPTION_KEY=%s\n' "$(.venv/bin/python -m app.core.keys)" > .env
	echo "Created backend/.env with a new encryption key. Back it up securely: losing it makes stored scans unreadable."
else
	echo "backend/.env already exists. Keeping your encryption key."
fi

.venv/bin/python -m app.db.migrate
.venv/bin/python -m app.db.seed
echo "Backend ready. Start it with: npm run dev:api (and npm run dev:worker for jobs)"
