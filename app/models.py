from django.db import models

# Create your models here.

class RSSFeed(models.Model):
    title = models.CharField(max_length=255)
    site_name = models.CharField(max_length=255)
    url = models.URLField()
    last_fetched = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.title

class Job(models.Model):
    title = models.CharField(max_length=255)
    company = models.CharField(max_length=255)
    location = models.CharField(max_length=255)
    description = models.TextField()
    pub_date = models.DateTimeField()
    link = models.URLField()
    rss_feed = models.ForeignKey(RSSFeed, on_delete=models.CASCADE)
    
    def __str__(self):
        return self.title
    