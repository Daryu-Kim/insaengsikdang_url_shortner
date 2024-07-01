from django.db import models

class ShortUrl(models.Model):
    short_url = models.CharField(max_length=6, unique=True)
    original_url = models.URLField()
