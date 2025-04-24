# backend/asgi.py
import os
from channels.routing import ProtocolTypeRouter, URLRouter
from django.core.asgi import get_asgi_application
from channels.auth import AuthMiddlewareStack

# from users.routing import websocket_urlpatterns  # هنعمل الملف ده لاحقاً
from apps.notifications.routing import websocket_urlpatterns

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "hnu_addmission.settings")

application = ProtocolTypeRouter(
    {
        "http": get_asgi_application(),
        "websocket": AuthMiddlewareStack(URLRouter(websocket_urlpatterns)),
    }
)
