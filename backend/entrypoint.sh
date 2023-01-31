#!/bin/sh
python3 manage.py migrate
python3 manage.py collectstatic
#python3 manage.py loaddata fixtures.json
exec "$@"
