import time
from ..app import app

@app.task(autoretry_for=(Exception,), retry_backoff=True, retry_backoff_max=1800, max_retries=5)
def first_task():
    pass
