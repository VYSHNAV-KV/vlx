from django.urls import re_path
from webapp import consumers

websocket_urlpatterns = [
    re_path(r'ws/chat/(?P<buyer>\w+)/(?P<seller>\w+)/$', consumers.ChatConsumer.as_asgi()),
]
