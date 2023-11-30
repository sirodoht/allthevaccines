#!/usr/local/bin/bash

set -e
set -x

# make sure latest requirements are installed
pip install -r requirements.txt

# make sure tests pass
python manage.py test

# push origins
git push origin main

# make sure lint passes
make lint

# generate static files
python manage.py collectstatic --noinput

# pull and reload on server
ssh root@allthevaccines.org 'cd /opt/apps/allthevaccines \
    && git pull \
    && source venv/bin/activate \
    && pip install -r requirements.txt \
    && python manage.py collectstatic --noinput \
    && python manage.py migrate \
    && touch /etc/uwsgi/vassals/allthevaccines.ini'
