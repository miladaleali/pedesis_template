#! /usr/bin/env bash
python /app/app/celeryworker_pre_start.py

# celery worker -A app.worker -l info -Q main-queue -c 1
python manage.py run celery