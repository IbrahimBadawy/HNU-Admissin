from django.urls import path, include
from rest_framework.routers import DefaultRouter




# coordination/urls.py
router = DefaultRouter()

urlpatterns = [
    path('', include(router.urls)),
]