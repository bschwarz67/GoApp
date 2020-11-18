from django.contrib import admin
from django.urls import include, path
urlpatterns = [
	path('board/', include('board.urls', namespace='board')),
    path('admin/', admin.site.urls),
	path('home/', include('home.urls', namespace='home')),
	path('accounts/', include('accounts.urls')),
	path('accounts/', include('django.contrib.auth.urls')),
]
