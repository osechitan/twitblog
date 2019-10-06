from django.db import models
from django.utils import timezone

class User(models.Model):
    userId = models.IntegerField()
    twitterId = models.CharField(primary_key=True,max_length=15)
    oauth_token = models.CharField(max_length=100)
    oauth_token_secret = models.CharField(max_length=100)
    created_date = models.DateTimeField(default=timezone.now)
