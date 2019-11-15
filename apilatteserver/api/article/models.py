from django.db import models
from django.utils import timezone
from datetime import datetime, timedelta

class Article(models.Model):
    # id = models.PositiveSmallIntegerField(primary_key=True)
    title = models.CharField(max_length=255)
    content = models.TextField(blank=True)
    badges = models.CharField(max_length=255, blank=True)
    slug = models.SlugField(max_length=255, blank=True)
    author = models.CharField(max_length=255)
    create_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)
    is_archived = models.BooleanField(default=False)
    img_url = models.CharField(max_length=255, blank=True)
    show_on_carousel = models.BooleanField(default=False)

    def __str__(self):
        if len(self.title) > 10:
            return str(self.id) + '_' + self.title[:10] + '...'
        else:
            return str(self.id) + '_' + self.title