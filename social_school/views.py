from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.shortcuts import render
from django.views.generic import ListView


class HomePage(LoginRequiredMixin, ListView):
    template_name = 'social_school/index.html'
    context_object_name = 'users_list'

    def get_queryset(self):
        return User.objects.all()

