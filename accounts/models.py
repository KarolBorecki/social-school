from django.contrib.auth.models import User
from django.db import models
from django.utils import timezone

from social_school.settings import NOTIFICATION_TYPES


class Profile(models.Model):
    user = models.OneToOneField(User, related_name='profile')

    def __str__(self):
        return self.user.username

    def request_as_friend(self, sender):
        friend, created = Friend.objects.get_or_create(sender=sender, invited=self, is_accepted=False)
        friend.save()

    def accept_as_friend(self, friend):
        friend.is_accepted = True
        to_friend, created = Friend.objects.get_or_create(sender=self, invited=friend.sender, is_accepted=True)

        friend.save()
        to_friend.save()

    @staticmethod
    def do_not_accept_as_friend(friend):
        friend.delete()

    def remove_from_friends(self, friend, is_done=False):
        Friend.objects.filter(sender=self, invited=friend).delete()

        if not is_done:
            friend.remove_from_friends(self, True)

    def get_friends(self):
        return self.friends.all()

    def get_friendships_requests(self):
        return self.notifications.filter(notification_type=NOTIFICATION_TYPES['friendship request']).all()


class Friend(models.Model):
    sender = models.ForeignKey(Profile, related_name='friends')
    invited = models.ForeignKey(Profile)
    is_accepted = models.BooleanField(default=False)
    date_of_friend = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.sender.__str__() + " and " + self.invited.__str__() + " Friendship"
