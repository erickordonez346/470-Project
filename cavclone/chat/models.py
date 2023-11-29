from datetime import datetime
from django.db import models


# Create your models here.
class Query(models.Model):
    content = models.TextField()
    response = models.TextField()
    audio_path = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)


class Activity(models.Model):
    enter_time = models.DateTimeField()
    exit_time = models.DateTimeField(null=True, blank=True)
