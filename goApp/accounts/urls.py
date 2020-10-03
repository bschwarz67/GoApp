from django.urls import path, re_path
from django.contrib.auth import views as auth_views

from . import views

app_name = 'accounts'
urlpatterns = [
	path('signup/', views.signup, name='signup'),
	path('login/', auth_views.LoginView.as_view(extra_context={'next': '/home/'})),
]
