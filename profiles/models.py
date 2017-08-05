from django.db import models
from django.utils import timezone

from accounts.models import Profile


class Notification(models.Model):
    text = models.CharField(max_length=200)
    sender = models.ForeignKey(Profile)
    send_date = models.DateTimeField(default=timezone.now)
