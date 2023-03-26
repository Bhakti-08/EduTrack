from django.urls import path
from .consumers import QuizConsumer

websocket_urlpatterns = [
    path("ws/save", QuizConsumer.as_asgi()),
]