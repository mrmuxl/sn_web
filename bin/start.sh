#!/bin/sh
export RUN_ENV=deploy
ERROR_LOG_FILE=/var/log/nginx/gevent_error.log
ACCESS_LOG_FILE=/var/log/nginx/gevent_access.log
python ../manage.py run_gunicorn -k gevent -w 8 -t 600 -u admin -g admin  --max-requests=1000 --preload --worker-connections=2000 --log-level=debug --error-logfile=${ERROR_LOG_FILE} --access-logfile=${ACCESS_LOG_FILE} --pid=gunicorn.pid -D
