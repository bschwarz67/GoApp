from django.urls import path, re_path

from . import views

app_name = 'home'
urlpatterns = [
	path('', views.index, name='index'),
	path('createTempPlayer/', views.createTempPlayer, name='createTempPlayer'),
	path('changePlayerColor/', views.changePlayerColor, name='changePlayerColor'),
]

