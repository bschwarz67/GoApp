from django.urls import path, re_path

from . import views

app_name = 'home'
urlpatterns = [
	path('', views.index, name='index'),
	path('logNewPlayerIn/<str:newUserUsername>/', views.logNewPlayerIn, name='logNewPlayerIn'),
	#path('changePlayerColor/', views.changePlayerColor, name='changePlayerColor'),
	#path('createTempPlayer/', views.createTempPlayer, name='createTempPlayer'),
]

