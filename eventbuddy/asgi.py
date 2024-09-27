import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'eventbuddy.settings')

from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter, URLRouter

app =  get_asgi_application()
from channels.auth import AuthMiddlewareStack
import Chat.routing  # Ensure the routing module is correct


application = ProtocolTypeRouter({
    "http": app,
    "websocket": AuthMiddlewareStack(
        URLRouter(
            Chat.routing.websocket_urlpatterns
        )
    ),
})
