#!/usr/bin/env bash
set -euo pipefail
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
if [ ! -f portal/migrations/0001_initial.py ]; then
  echo "ERROR: portal/migrations/0001_initial.py is missing. Stop deployment and create/check migrations locally first."
  exit 1
fi
python manage.py check
python manage.py collectstatic --no-input
python manage.py migrate
