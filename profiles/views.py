from django.contrib.auth.models import User
from django.shortcuts import render
from django.utils.decorators import method_decorator
from django.views import generic
from django.views.decorators.csrf import csrf_protect, csrf_exempt


class AllUsersList(generic.ListView):
    template_name = 'profiles/all_users_list.html'
    model = User


class UserDetailsView(generic.View):
    template_name = "profiles/user_detail.html"
    model = User

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name)

    def post(self, request, *args, **kwargs):
        user = User.objects.filter(id=self.kwargs.get('pk'))



