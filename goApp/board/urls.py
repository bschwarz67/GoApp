from django.urls import path, re_path

from . import views

app_name = 'board'
urlpatterns = [
	path('', views.index, name='index'),
	re_path(r'^(?P<gameIdSlug>.*)/$', views.index, name='createdGame'),
	#path('<str:gameIdSlug>/', views.index, name='createdGame'),
	path('play/', views.play, name='play'),
]