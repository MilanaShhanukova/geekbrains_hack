#! /usr/bin/env bash
set -e

exec celery --app=worker.beat:app beat --loglevel=DEBUG --pidfile /tmp/celerybeat.pid -s /tmp/celerybeat-schedule
