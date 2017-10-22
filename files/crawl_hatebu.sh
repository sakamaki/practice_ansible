#!/usr/bin/env bash

cd /app/practice_d3
source ../appenv/bin/activate
python manage.py crawl --date 20171001
python manage.py crawl --date 20171002
python manage.py crawl --date 20171003
python manage.py crawl --date 20171004
python manage.py crawl --date 20171005
python manage.py crawl --date 20171006
python manage.py crawl --date 20171007
python manage.py crawl --date 20171008
python manage.py crawl --date 20171009
