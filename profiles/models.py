from django.contrib.auth.models import User
from django.db import models
from django.utils import timezone

from social_school.settings import NOTIFICATION_TYPES


class Notification(models.Model):
    text = models.CharField(max_length=200)
    from_user = models.ForeignKey(User, related_name='notifications_send_by_self', default=None)
    to_user = models.ForeignKey(User, related_name='notifications', default=None)
    send_date = models.DateTimeField(default=timezone.now)
    notification_type = models.CharField(max_length=15, default=NOTIFICATION_TYPES['private message'])

    def __str__(self):
        return self.notification_type + " to " \
               + self.to_user.__str__() + " from " + self.from_user.__str__()
