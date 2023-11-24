from celery.schedules import crontab
from .app import app



# @app.on_after_configure.connect
# def setup_periodic_tasks(sender, **kwargs):
#     sender.add_periodic_task(crontab(hour=23, minute=0), update_all_task.s(), name='update all products info')
