#!/bin/bash

python manage.py makemigrations
python manage.py migrate --no-input

# mkdir static & mkdir media

python manage.py collectstatic --no-input
python manage.py loaddata data.json