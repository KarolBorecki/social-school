from django.contrib.auth.models import User
from django.views import generic


class AllUsersList(generic.ListView):
    template_name = 'profiles/all_users_list.html'
    model = User


class UserDetailsView(generic.DetailView):
    template_name = "profiles/user_detail.html"
    model = User
