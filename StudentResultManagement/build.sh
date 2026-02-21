#!/usr/bin/env bash
set -o errexit

pip install -r requirements.txt

python manage.py collectstatic --no-input

python manage.py migrate

if [[ $DJANGO_SUPERUSER_USERNAME ]]; then
  echo "Attemping to create superuser..."
  python manage.py createsuperuser \
    --no-input \
    --username $DJANGO_SUPERUSER_USERNAME \
    --email $DJANGO_SUPERUSER_EMAIL || echo "Superuser creation skipped (it might already exist or the password didn't meet requirements)."
fi