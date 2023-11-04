from django.urls import path
from .consumers import *

websocket_urlpatterns = [
    path('community/broadcast', CommunityConsumer.as_asgi())
]
