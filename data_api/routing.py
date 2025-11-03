from django.urls import path
from . import consumers

websocket_urlpatterns = [
    path("ws/topics/", consumers.TopicConsumer.as_asgi()),
]
