from django.db import models
from django.utils import timezone

from accounts.models import Profile
from social_school.settings import NOTIFICATION_TYPES


class Notification(models.Model):
    text = models.CharField(max_length=200)
    from_user = models.ForeignKey(Profile)
    to_user = models.ForeignKey(Profile, related_name='notifications', default=None)
    send_date = models.DateTimeField(default=timezone.now)
    notification_type = models.CharField(max_length=15, default=NOTIFICATION_TYPES['private message'])