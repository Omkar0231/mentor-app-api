#!/usr/bin/env bash
# exit on error
set -o errexit

pip install -r requirements.txt

python manage.py collectstatic --no-input
python manage.py migrate
if [[ $CREATE_SUPERUSER ]];
then
  python manage.py createsuperuser --no-input --email "tg6398119861@gmail.com"
fi