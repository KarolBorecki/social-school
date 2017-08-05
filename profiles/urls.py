from django.conf.urls import url
from . import views

app_name = 'profiles'

urlpatterns = [
    url(r'^users/$', views.AllUsersList.as_view(), name='users_list'),
    #url(r'^users/$', views.UserDetailsView.as_view(), name='user_detail'),
]
