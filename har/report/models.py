from django.db import models
from django.contrib.auth.models import User

# Report model
class Report(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.TextField()
    latitude = models.FloatField()
    longitude = models.FloatField()
    altitude = models.FloatField()
    accuracy = models.FloatField(null=True, blank=True)
    creation_time = models.DateTimeField(auto_now=True)
    update_time = models.DateTimeField(auto_now=True)
