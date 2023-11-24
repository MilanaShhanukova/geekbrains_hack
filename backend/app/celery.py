from celery import Celery
import os

REDIS_URL = os.getenv("REDIS_URL")

celery_app = Celery(
    'worker',
    broker=f'{REDIS_URL}/14',
    backend=f'{REDIS_URL}/15',
    include=['worker.tasks']
)
celery_app.conf.broker_transport_options = {'visibility_timeout': 60 * 15}  # 15 minutes
