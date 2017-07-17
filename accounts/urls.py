from django.conf.urls import url
from django.contrib.auth import views as auth_views

from accounts import views

app_name = 'accounts'

urlpatterns = [
    url(r'^$', views.IndexView.as_view(), name='index'),
    url(r'^login/$', auth_views.login, {'template_name': 'accounts/login.html'}, name='login'),
    url(r'^logout/$', auth_views.logout, {'template_name': 'accounts/index.html'}, name='logout'),
    url(r'^active/(?P<user_id>[0-9]+)/$', views.email_activation_view, name='email activation'),
    url(r'^password_reset/$', views.PasswordResetView.as_view(), name='password_reset'),
    url(r'^register/$', views.RegisterView.as_view(), name='register'),
]
