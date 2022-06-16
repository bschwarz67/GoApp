from django.urls import re_path

from . import consumers

websocket_urlpatterns = [
    re_path('ws/challenge/', consumers.ChallengeConsumer.as_asgi()),
]