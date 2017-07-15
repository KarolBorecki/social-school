from django.db import models
from django.utils.text import slugify
from django.contrib.auth.models import User
# Create your models here.


class Group(models.Model):
    name = models.CharField(max_length=255, unique=True)
    slug = models.SlugField(allow_unicode=True, unique=True)
    description = models.TextField(blank=True, default='')
    members = models.ManyToManyField(User, through='GroupMember')

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super(models.Model, self).save(*args, **kwargs)

    def __str__(self):
        return self.name


class GroupMember(models.Model):
    group = models.ForeignKey(Group, related_name='memberships')
    user = models.ForeignKey(User, related_name='user_groups')

    def __str__(self):
        return self.user.username

    class Meta:
        unique_together = ('group', 'user')
