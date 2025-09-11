# your_app/routing.py

from django.urls import path

from Member.consumers import *

websocket_urlpatterns = [
    path('ws/chat/', ChatConsumer.as_asgi()),
]
