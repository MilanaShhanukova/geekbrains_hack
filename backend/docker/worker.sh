#! /usr/bin/env bash
set -e

exec watchmedo auto-restart --directory=/opt/app/ --pattern=*.py --recursive -- celery --app=worker.app:app worker --loglevel=INFO --concurrency=6 -n worker1%h