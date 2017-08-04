from django.conf.urls import url
from . import views

app_name = 'profiles'

urlpatterns = [
    url(r'^users/$', views.AllUsersList.as_view(), name='users_list'),
]
