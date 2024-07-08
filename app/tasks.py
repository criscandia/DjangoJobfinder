from celery import shared_task
from .models import RSSFeed, Job
import feedparser
from celery.signals import task_success, task_failure
import logging
from dateutil import parser as date_parser
from django.utils import timezone


logger = logging.getLogger("celery")


@shared_task
def update_rss_feeds():
    try:
        feeds = RSSFeed.objects.all()
        for feed in feeds:
            d = feedparser.parse(feed.url)
            for entry in d.entries:
                title = entry.get("title", "")
                link = entry.get("link", "")
                description = entry.get("description", "")
                pub_date = None
                if pub_date_str := entry.get("published"):
                    pub_date = date_parser.parse(pub_date_str)
                    if timezone.is_naive(pub_date):
                        pub_date = timezone.make_aware(pub_date)
                job, created = Job.objects.update_or_create(
                    title=title,
                    company=feed.site_name,
                    location="",
                    defaults={
                        "description": description,
                        "pub_date": pub_date,
                        "link": link,
                        "rss_feed": feed,
                    },
                )
        logger.info("RSS feeds updated successfully")
    except Exception as e:
        logger.error(f"Error in update_rss_feeds: {e}")
        raise e


@task_success.connect
def task_success_handler(sender=None, result=None, **kwargs):
    logger.info(f"Tarea {sender.name} ejecutada con éxito: {result}")


@task_failure.connect
def task_failure_handler(sender=None, task_id=None, exception=None, **kwargs):
    logger.error(f"Tarea {sender.name} falló: {str(exception)}")
