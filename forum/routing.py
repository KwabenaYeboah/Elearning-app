from django.urls import re_path

from .consumers import ForumConsumer

websocket_urlpatterns = [
    re_path(r'ws/forum/(?P<course_id>\d+)/$', ForumConsumer),
]