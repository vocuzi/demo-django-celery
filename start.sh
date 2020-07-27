#!/usr/bin/env bash
service rabbitmq-server restart
service nginx restart
gunicorn project.wsgi --bind 0.0.0.0:8010 --workers 4 --daemon
celery -A project worker -l info