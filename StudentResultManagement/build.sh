#!/usr/bin/env bash
set -o errexit

pip install -r requirements.txt

python manage.py collectstatic --no-input

python manage.py migrate

# Use the custom script to ensure the superuser exists with the correct password
python ensure_superuser.py