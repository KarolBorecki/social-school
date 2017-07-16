from django.conf.urls import url
from django.contrib.auth import views as auth_views

from accounts import views

app_name = 'accounts'

urlpatterns = [
    url(r'^login/', views.LoginView.as_view(), name='login'),
    url(r'^logout/', auth_views.logout, {'template_name': 'accounts/index.html'}, name='logout'),
    url(r'^register/', views.RegisterView.as_view(), name='register'),
]
