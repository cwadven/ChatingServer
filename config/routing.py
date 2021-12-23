from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter, URLRouter
from websocket.routing import websocket_urlpatterns

application = ProtocolTypeRouter({
    'websocket': AuthMiddlewareStack(
        # URLRouter 로 연결, 소비자의 라우트 연결 HTTP path 조사
        URLRouter(
            websocket_urlpatterns
        )
    ),
})
