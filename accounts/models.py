from django.contrib.auth.models import User
from django.db import models

from profiles.models import Notification
from social_school.settings import NOTIFICATION_TYPES, FRIENDSHIP_REQUEST_TEXT


class Profile(models.Model):
    user = models.OneToOneField(User, related_name='profile')
    friends = models.ManyToManyField(User, related_name='friends', default=None)

    def __str__(self):
        return self.user.username

    def request_as_friend(self, user):
        notification, created = Notification.objects\
            .get_or_create(from_user=self.user, to_user=user,
                           text=FRIENDSHIP_REQUEST_TEXT, notification_type=NOTIFICATION_TYPES['friendship request'])
        notification.save()

    def accept_as_friend(self, user):
        self.user.notifications\
            .filter(from_user=user, notification_type=NOTIFICATION_TYPES['friendship request']).delete()
        self.friends.add(user)
        user.profile.friends.add(self.user)

    def do_not_accept_as_friend(self, user):
        self.user.notifications \
            .filter(from_user=user, notification_type=NOTIFICATION_TYPES['friendship request']).delete()

    def remove_from_friends(self, user):
        self.friends.remove(user)
        user.profile.friends.remove(self.user)

    def get_friends(self):
        return self.friends.all()

    def is_friend(self, user):
        if user in self.get_friends():
            return True
        return False

    def get_friendships_requests(self):
        return self.user.notifications.filter(notification_type=NOTIFICATION_TYPES['friendship request']).all()
