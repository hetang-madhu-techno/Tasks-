# all_topics/asgi.py
import os
from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack
import data_api.routing

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'all_topics.settings')

application = ProtocolTypeRouter({
    "http": get_asgi_application(),
    "websocket": AuthMiddlewareStack(
        URLRouter(
            data_api.routing.websocket_urlpatterns
        )
    ),
})
