#!/bin/sh
export RUN_ENV=deploy
python ../manage.py run_gunicorn -k gevent -w 10 -t 600  --max-requests=1000 --preload --worker-connections=2000 -D --pid=gunicorn.pid
