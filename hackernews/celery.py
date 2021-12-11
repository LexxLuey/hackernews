import os
from celery import Celery

# set the default Django settings module for the 'celery' program.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'hackernews.settings')

app = Celery('hackernews', broker='pyamqp://guest@localhost//')

app.config_from_object('django.conf:settings', namespace='CELERY')

app.autodiscover_tasks()


@app.task(bind=True)
def debug_task(self):
    print('Request: {0!r}'.format(self.request))


app.conf.beat_schedule = {
    # Scheduler Name
    'get-latest-news': {
        # Task Name (Name Specified in Decorator)
        'task': 'get_latest_news',
        # Schedule
        'schedule': 300.0,
    },
}
