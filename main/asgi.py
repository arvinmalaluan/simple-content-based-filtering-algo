import errands.routing
from django.core.asgi import get_asgi_application
from chat.routing import websocket_urlpatterns
from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter, URLRouter
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'main.settings')
django.setup()


django_asgi_application = get_asgi_application()

application = ProtocolTypeRouter(
    {
        'http': django_asgi_application,
        'websocket': AuthMiddlewareStack(
            URLRouter(
                websocket_urlpatterns
            )
        )
    }
)
