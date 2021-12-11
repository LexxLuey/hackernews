import requests
from celery.app import task, shared_task
from celery.schedules import crontab

from news.helpers import get_latest_news_query, get_item_by_id, create_story_item, create_generic_item, create_job_item, \
    create_poll_item, create_poll_options_item
from news.models import Story, HackerNewsItem, Job, Poll, PollOption


@shared_task(name="get_latest_news")
def get_latest_news():
    try:
        data = get_latest_news_query()
        for item in data:
            news_item = get_item_by_id(item)
            if news_item['type'] == 'story':
                if Story.objects.filter(id=news_item['id']).exists() or HackerNewsItem.objects.filter(
                        id=news_item['id']).exists():
                    print(f"ID {news_item['id']} already exists! Skipping")
                    continue
                else:
                    create_story_item(news_item)
                    create_generic_item(news_item)

            elif news_item['type'] == 'job':
                if Job.objects.filter(id=news_item['id']).exists():
                    print(f"ID {news_item['id']} already exists! Skipping")
                    continue
                else:
                    create_job_item(news_item)
                    create_generic_item(news_item)

            elif news_item['type'] == 'poll':
                if Poll.objects.filter(id=news_item['id']).exists():
                    print(f"ID {news_item['id']} already exists! Skipping")
                    continue
                else:
                    create_poll_item(news_item)
                    create_generic_item(news_item)

            elif news_item['type'] == 'pollopt':
                if PollOption.objects.filter(id=news_item['id']).exists():
                    print(f"ID {news_item['id']} already exists! Skipping")
                    continue
                else:
                    create_poll_options_item(news_item)

            else:
                pass
        print(f"successfully retrieved and updated DB")
    except Exception as e:
        print(f"The following error occured: {e}")
