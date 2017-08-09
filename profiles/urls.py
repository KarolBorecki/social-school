from django.conf.urls import url
from . import views

app_name = 'profiles'

urlpatterns = [
    url(r'^all_users/$', views.AllUsersListView.as_view(), name='users_list'),
    url(r'^friends/$', views.FriendsListView.as_view(), name='friends_list'),
    url(r'^user/(?P<pk>[0-9]+)/$', views.UserDetailView.as_view(), name='user_detail'),
]
