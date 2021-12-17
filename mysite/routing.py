from channels.auth import AuthMiddleWareStack
from channels.routing import ProtocolTypeRouter, URLRouter 

from forum import routing

application = ProtocolTypeRouter({
    'websocket':AuthMiddleWareStack(
        URLRouter(routing.websocket_urlpatterns)
    ),
})