#!/usr/bin/env bash

cd /app/practice_d3
source ../appenv/bin/activate
python manage.py migrate
