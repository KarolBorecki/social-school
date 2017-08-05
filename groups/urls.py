from django.conf.urls import url
from . import views

app_name = 'groups'

urlpatterns = [
    url(r'^$', views.GroupListView.as_view(), name='list'),
    url(r'^new/$', views.CreateGroupView.as_view(), name='create_group'),
    url(r'^join/(?P<slug>[-\w]+)/$', views.JoinGroupView.as_view(), name='join_group'),
    url(r'^leave/(?P<slug>[-\w]+)/$', views.LeaveGroupView.as_view(), name='leave'),
    url(r'^(?P<slug>[-\w]+)/$', views.GroupIndexView.as_view(), name='index'),
    url(r'^posts/(?P<pk>[\w-]+)/$', views.PostView.as_view(), name='post_details'),
]
