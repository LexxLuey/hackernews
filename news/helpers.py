import datetime
import requests
from .models import Story, Job, Poll, PollOption, HackerNewsItem, Comment

payload = "{}"


def get_latest_news_query():
    try:
        url = "https://hacker-news.firebaseio.com/v0/topstories.json"
        response = requests.request("GET", url, data=payload)
        return response.json()
    except Exception as e:
        print(f"The following error occurs:\n{e}")


def get_item_by_id(item_id):
    try:
        url = f"https://hacker-news.firebaseio.com/v0/item/{item_id}.json"
        response = requests.request("GET", url, data=payload)
        return response.json()
    except Exception as e:
        print(f"The following error occurs:\n{e}")


def convert_unix_time(unix_time):
    timestamp = datetime.datetime.fromtimestamp(unix_time)
    return timestamp.strftime('%Y-%m-%d')


def check_for_missing_data(news_item):
    keys = ['id', 'type', 'by', 'title', 'url',
            'score', 'descendants', 'time', 'text', 'kids',
            'parts', 'parent']
    # for key, value in news_item.items():
    for key in keys:
        if key not in news_item:
            news_item[key] = None


def create_story_item(news_item):
    date_created = convert_unix_time(news_item['time'])
    check_for_missing_data(news_item)
    try:
        story = Story.objects.create(id=news_item['id'], type=news_item['type'],
                                     author=news_item['by'], created=date_created,
                                     title=news_item['title'], comment_count=news_item['descendants'],
                                     score=news_item['score'], url=news_item['url'])
    except Exception as e:
        print(f"The following error occurs in create_story_item({news_item}):{e}")
    else:
        story.save()
        print(f"{news_item['type']} created")
    if news_item.get('kids') is not None:
        for comment_id in news_item['kids']:
            try:
                create_comment(comment_id)
                print(f"{comment_id['type']} created")
            except Exception as e:
                print(f"The following error occurs in create_story_item({news_item})->create_comment({comment_id}:{e}")


def create_job_item(news_item):
    date_created = convert_unix_time(news_item['time'])
    check_for_missing_data(news_item)
    try:
        job = Job.objects.create(id=news_item['id'], type=news_item['type'],
                                 author=news_item['by'], created=date_created,
                                 title=news_item['title'], score=news_item['score'],
                                 url=news_item['url'])
    except Exception as e:
        print(f"The following error occurs in create_job_item({news_item}):{e}")
    else:
        job.save()
        print(f"{news_item['type']} created")
    if news_item.get('kids') is not None:
        for comment_id in news_item['kids']:
            try:
                create_comment(comment_id)
            except Exception as e:
                print(f"The following error occurs in create_job_item({news_item})->create_comment({comment_id}:{e}")


def create_poll_item(news_item):
    date_created = convert_unix_time(news_item['time'])
    check_for_missing_data(news_item)
    poll = None
    try:
        poll = Poll.objects.create(id=news_item['id'], type=news_item['type'],
                                   author=news_item['by'], created=date_created,
                                   title=news_item['title'], comment_count=news_item['descendants'],
                                   content=news_item['text'], url=news_item['url'],
                                   score=news_item['score'])
    except Exception as e:
        print(f"The following error occurs in create_poll_item({news_item}):{e}")
    else:
        print(f"{news_item['type']} created")
        poll.save()
    if news_item.get('kids') is not None:
        for comment_id in news_item['kids']:
            try:
                create_comment(comment_id)
            except Exception as e:
                print(f"The following error occurs in create_poll_item({news_item})->create_comment({comment_id}:{e}")
    if news_item.get('parts') is not None:
        for pollops in news_item['parts']:
            create_poll_options_item(pollops, poll)


def create_poll_options_item(parts, poll=None):
    try:
        pollopts = get_item_by_id(parts)
    except Exception as e:
        print(f"The following error occurs in get_item_by_id({parts}):{e}")

    for opt in pollopts:
        date_created = convert_unix_time(opt['time'])
        check_for_missing_data(opt)
        try:
            if poll is None:
                option = PollOption.objects.create(id=opt['id'], type=opt['type'],
                                                   author=opt['by'], created=date_created,
                                                   comment_count=opt['descendants'], score=opt['score'],
                                                   url=opt['url'])
            else:
                option = PollOption.objects.create(id=opt['id'], type=opt['type'],
                                                   author=opt['by'], created=date_created,
                                                   comment_count=opt['descendants'], score=opt['score'],
                                                   poll=poll, url=opt['url'])
        except Exception as e:
            print(f"The following error occurs in create_poll_options_item({opt}):{e}")

        else:
            option.save()
            print(f"{opt['type']} created")

        if opt.get('kids') is not None:
            for comment_id in opt['kids']:
                try:
                    create_comment(comment_id)
                except Exception as e:
                    print(
                        f"The following error occurs in create_poll_options_item({opt})->create_comment({comment_id}:{e}")


def create_comment(comment_id):
    comment = get_item_by_id(comment_id)
    date_created = convert_unix_time(comment['time'])
    check_for_missing_data(comment)
    try:
        if comment.get('parent') is not None:
            if comment['parent'] in comment.values():
                if Story.objects.filter(id=comment['id']).exists():
                    print(f"ID {comment['id']} already exists! Skipping")
                else:
                    item_comment = Comment.objects.create(id=comment['id'], type=comment['type'],
                                                          author=comment['by'], created=date_created,
                                                          parent_comment=comment['parent'], content=comment['text'])
                    item_comment.save()
        else:
            if Story.objects.filter(id=comment['id']).exists():
                print(f"ID {comment['id']} already exists! Skipping")
            else:
                item_comment = Comment.objects.create(id=comment['id'], type=comment['type'],
                                                      author=comment['by'], created=date_created,
                                                      content=comment['text'])
                item_comment.save()
    except Exception as e:
        print(f"The following error occurs in create_comment({comment_id}):{e}")


def create_generic_item(item):
    date_created = convert_unix_time(item['time'])
    if item['type'] == 'story':
        check_for_missing_data(item)
        generic_item = HackerNewsItem.objects.create(id=item['id'], type=item['type'],
                                                     author=item['by'], created=date_created,
                                                     title=item['title'], comment_count=item['descendants'],
                                                     url=item['url'], score=item['score'])

        generic_item.save()

    if item['type'] == 'job':
        check_for_missing_data(item)
        generic_item = HackerNewsItem.objects.create(id=item['id'], type=item['type'],
                                                     author=item['by'], created=date_created,
                                                     title=item['title'], score=item['score'],
                                                     url=item['url'])
        generic_item.save()

    if item['type'] == 'poll':
        check_for_missing_data(item)
        generic_item = HackerNewsItem.objects.create(id=item['id'], type=item['type'],
                                                     author=item['by'], created=date_created,
                                                     title=item['title'], comment_count=item['descendants'],
                                                     content=item['text'], url=item['url'],
                                                     score=item['score'])
        generic_item.save()

    if item['type'] == 'pollopt':
        pass



