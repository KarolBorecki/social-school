from django.conf.urls import url
from . import views

app_name = 'groups'

urlpatterns = [
    url(r'^$', views.GroupListView.as_view(), name='group_list'),
    url(r'^new/$', views.CreateGroupView.as_view(), name='create_group'),
    url(r'^join/(?P<slug>[-\w]+)/$', views.JoinGroupView.as_view(), name='join_group'),
    url(r'^(?P<slug>[-\w]+)/add_users/$', views.AddUserToGroupView.as_view(), name='add_user'),
    url(r'^leave/(?P<slug>[-\w]+)/$', views.LeaveGroupView.as_view(), name='leave'),
    url(r'^(?P<slug>[-\w]+)/$', views.GroupIndexView.as_view(), name='group_timeline'),
    url(r'^posts/(?P<pk>[\w-]+)/$', views.PostDetailView.as_view(), name='post_details'),
]
