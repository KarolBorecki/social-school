from django.contrib.auth.models import User
from django.shortcuts import redirect
from django.views import generic

from accounts.models import Profile
from profiles.models import Notification
from social_school.settings import FRIENDSHIP_REQUEST_TEXT, NOTIFICATION_TYPES


class AllUsersListView(generic.ListView):
    template_name = 'profiles/all_users_list.html'
    model = User


class FriendsListView(generic.ListView):
    template_name = 'profiles/users_friends.html'
    model = User


class UserDetailView(generic.DetailView):
    template_name = "profiles/user_detail.html"
    model = User

    def post(self, request, *args, **kwargs):
        profile = Profile.objects.filter(user=User.objects.filter(id=self.kwargs.get('pk'))).get()

        if 'add_friend' in request.POST:
            profile.request_as_friend(request.user.profile)
            invite, created = Notification.objects.\
                get_or_create(text=FRIENDSHIP_REQUEST_TEXT, from_user=request.user.profile,
                              to_user=profile, notification_type=NOTIFICATION_TYPES['friendship request'])
            invite.save()
        elif 'delete_friend' in request.POST:
            profile.remove_from_friends(request.user.profile)

        return redirect('profiles:users_list')
