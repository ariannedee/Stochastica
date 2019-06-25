from django.conf.urls import url

from . import consumers

websocket_urlpatterns = [
    url(r'^ws/play/(?P<game_id>\w+)/', consumers.ControllerConsumer),
]