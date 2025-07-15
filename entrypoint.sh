#/usr/bin/env sh

flask --app access.py db migrate 2>&1 | tee /var/log/pyGFAccess
flask --app access.py db upgrade 2>&1 | tee -a /var/log/pyGFAccess

/usr/local/bin/uwsgi --ini /pyGFAccess/uwsgi.ini