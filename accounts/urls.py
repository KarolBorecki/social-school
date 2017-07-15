from django.conf.urls import url
from django.contrib.auth import views as auth_views

from accounts import views

app_name = 'accounts'

urlpatterns = [
    url(r'^$', views.IndexView.as_view(), name='index'),
    url(r'^login/$', auth_views.login, {'template_name': 'login.html'}, name='login'),
    url(r'^logout/$', auth_views.logout, {'template_name': 'index.html'}, name='logout'),
    url(r'^register/$', views.register, name='register'),
]
