from django.urls import path, re_path

from . import views

app_name = 'home'
urlpatterns = [
	path('', views.index, name='index'),
	re_path(r'^playerMatch/*$', views.playerMatch, name='playerMatch'),
	path('createPlayer/', views.createPlayer, name='createPlayer'),
	path('changePlayerColor/', views.changePlayerColor, name='changePlayerColor'),
]

