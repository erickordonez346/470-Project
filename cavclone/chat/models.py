from django.db import models


# Create your models here.
class Query(models.Model):
    content = models.TextField()
    response = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
