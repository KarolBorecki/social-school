from django.contrib.auth.models import User
from django.db import models


class Profile(models.Model):
    user = models.ForeignKey(User)
    friends = models.ManyToManyField(User, related_name='friends')