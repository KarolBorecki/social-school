from django.conf.urls import url
from . import views

app_name = 'groups'

urlpatterns = [
    url(r'^$', views.GroupListView.as_view(), name='list'),
    url(r'^new/$', views.CreateGroupView.as_view(), name='create'),
    url(r'^join/(?P<slug>[-\w]+)/$', views.JoinGroupView.as_view(), name='join'),
    url(r'^leave/(?P<slug>[-\w]+)/$', views.LeaveGroupView.as_view(), name='leave'),
    url(r'^(?P<slug>[-\w]+)/$', views.GroupIndexView.as_view(), name='index'),
]
