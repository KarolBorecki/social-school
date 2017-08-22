from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.shortcuts import redirect, get_object_or_404
from django.utils.decorators import method_decorator
from django.views import generic
from django.views.decorators.csrf import csrf_protect

from profiles.exceptions import AlreadyInvitedException


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
        user = request.user
        friend = User.objects.filter(username=request.POST['friend_username']).get()

        if 'agree' in request.POST:
            user.profile.accept_as_friend(friend)
        elif 'dont_agree' in request.POST:
            user.profile.do_not_accept_as_friend(friend)
        return redirect('profiles:invites_list')


@method_decorator(csrf_protect, name='post')
class UserDetailView(generic.DetailView):
    template_name = "profiles/user_detail.html"
    model = User

    def post(self, request, *args, **kwargs):
        user = request.user
        friend = User.objects.filter(id=self.kwargs.get('pk')).get()

        if not friend.notifications.filter(from_user=user).exists():
            if 'add_friend' in request.POST:
                user.profile.request_as_friend(friend)

            elif 'delete_friend' in request.POST:
                user.profile.remove_from_friends(friend)
        else:
            #Need to think about better errors
            raise AlreadyInvitedException(friend)

        return redirect('profiles:user_detail', friend.id)
