# from django_cron import CronJobBase, Schedule
from .models import RSSFeed, Job
import feedparser
from dateutil import parser


class UpdateRSSFeedsCronJob(CronJobBase):
    RUN_EVERY_MINS = 1440  # Ejecutar cada 24 horas

    schedule = Schedule(run_every_mins=RUN_EVERY_MINS)
    code = "app.update_rss_feeds"  # Un código único para identificar este trabajo cron

    def do(self):
        feeds = RSSFeed.objects.all()
        for rss_feed in feeds:
            self.parse_rss(rss_feed)

    def parse_rss(self, rss_feed):
        parser_feed = feedparser.parse(rss_feed.url)
        for entry in parser_feed.entries:
            title = entry.get("title", "")
            link = entry.get("link", "")
            description = entry.get("description", "")
            pub_date = (
                parser.parse(entry.get("published", ""))
                if entry.get("published")
                else None
            )

            Job.objects.update_or_create(
                title=title,
                company=rss_feed.site_name,
                location="",
                description=description,
                pub_date=pub_date,
                link=link,
                rss_feed=rss_feed,
            )
