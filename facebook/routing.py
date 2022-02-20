import os

from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter, URLRouter
from django.core.asgi import get_asgi_application
from chat.consumers import ChatConsumer
from django.urls import path
# import chat.routing

# os.environ.setdefault("DJANGO_SETTINGS_MODULE", "mysite.settings")

application = ProtocolTypeRouter({
#   "http": get_asgi_application(),
  "websocket": AuthMiddlewareStack(
        URLRouter([
            path('ws/chat/<str:username>/', ChatConsumer.as_asgi()),]
        )
    ),
})