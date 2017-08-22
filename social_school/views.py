from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.views.generic import ListView


class HomePage(LoginRequiredMixin, ListView):
    template_name = 'social_school/index.html'
    context_object_name = 'posts'

    def get_queryset(self):
        user = self.request.user
        posts = []
        for group_membership in user.user_groups.all():
            posts += group_membership.group.posts.all()
        return posts

