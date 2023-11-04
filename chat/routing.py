from django.urls import path
from .consumers import *

from seekerFolder.consumers import *

websocket_urlpatterns = [
    path('get-my-convo/getmessages/<int:id>', ConvoConsumer.as_asgi()),
    path('get-my-convo/<int:id>', ChatConsumer.as_asgi()),

    # For testing
    path('getnumber/<int:id>', ChatConsumer.as_asgi()),
    path('community/broadcast', CommunityConsumer.as_asgi())
]
