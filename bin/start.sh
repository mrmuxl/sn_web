#!/bin/sh
export RUN_ENV=deploy
LOG_FILE=/var/log/nginx/kx.log
python ../manage.py run_gunicorn -k gevent -w 10 -t 600  --max-requests=1000 --preload --worker-connections=2000 --log-level=debug --error-logfile=${LOG_FILE} --pid=gunicorn.pid -D
