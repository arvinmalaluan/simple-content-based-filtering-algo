import os
import django
from django.core.asgi import get_asgi_application
from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter, URLRouter

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'main.settings')

django_asgi_application = get_asgi_application()

application = ProtocolTypeRouter(
    {
        'http': django_asgi_application,
        'websocket': AuthMiddlewareStack(
            URLRouter(
                # Import websocket_urlpatterns here, inside the URLRouter
                from chat.routing import websocket_urlpatterns
            )
        )
    }
)
