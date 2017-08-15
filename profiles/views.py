from django.contrib.auth.models import User
from django.shortcuts import redirect
from django.utils.decorators import method_decorator
from django.views import generic
from django.views.decorators.csrf import csrf_protect

from accounts.models import Profile, Friend
from profiles.models import Notification
from social_school.settings import FRIENDSHIP_REQUEST_TEXT, NOTIFICATION_TYPES


class AllUsersListView(generic.ListView):
    template_name = 'profiles/all_users_list.html'
    model = User


class FriendsListView(generic.ListView):
    template_name = 'profiles/users_friends.html'
    model = User


@method_decorator(csrf_protect, name='post')
class InvitesListView(generic.TemplateView):
    template_name = 'profiles/invites_list.html'

    def post(self, request, *args, **kwargs):
        user = request.user.profile
        sender = User.objects.filter(id=request.POST.get('friend_id', False)).get().profile
        friend = sender.friends.filter(invited=request.user.profile).get()

        if 'agree' in request.POST:
            user.accept_as_friend(friend)
        elif 'dont_agree' in request.POST:
            user.do_not_accept_as_friend(friend)

        friendship_request = Notification.objects.filter(notification_type=NOTIFICATION_TYPES['friendship request'],
                                                         from_user=sender, to_user=user)
        friendship_request.delete()
        return redirect('profiles:invites_list')


@method_decorator(csrf_protect, name='post')
class UserDetailView(generic.DetailView):
    template_name = "profiles/user_detail.html"
    model = User

    def post(self, request, *args, **kwargs):
        profile = Profile.objects.filter(user=User.objects.filter(id=self.kwargs.get('pk'))).get()
        friend_obj = profile.friends.filter(invited=request.user.profile)

        if 'add_friend' in request.POST:
            if not friend_obj.exists():
                profile.request_as_friend(request.user.profile)
                invite, created = Notification.objects.\
                    get_or_create(text=FRIENDSHIP_REQUEST_TEXT, from_user=request.user.profile,
                                  to_user=profile, notification_type=NOTIFICATION_TYPES['friendship request'])
                invite.save()
            else:
                request.user.profile.accept_as_friend(friend_obj.get())

        elif 'delete_friend' in request.POST:
            profile.remove_from_friends(request.user.profile)

        return redirect('profiles:users_list')
