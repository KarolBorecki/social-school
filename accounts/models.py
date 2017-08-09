from django.contrib.auth.models import User
from django.db import models
from django.utils import timezone


class Profile(models.Model):
    user = models.OneToOneField(User, related_name='profile')

    def __str__(self):
        return self.user.username

    def add_as_friend(self, user, is_done=False):
        friend, created = Friend.objects.get_or_create(user=self, friend=user)
        friend.save()

        if not is_done:
            user.add_as_friend(self, True)

    def remove_from_friends(self, user, is_done=False):
        Friend.objects.filter(user=self, friend=user).delete()

        if not is_done:
            user.remove_from_friends(self, True)

    def get_friends(self):
        return Friend.objects.filter(user=self).all()


class Friend(models.Model):
    user = models.ForeignKey(Profile, related_name='friends')
    friend = models.ForeignKey(Profile)
    date_of_friend = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.user.__str__() + " and " + self.friend.__str__() + " Friendship"
