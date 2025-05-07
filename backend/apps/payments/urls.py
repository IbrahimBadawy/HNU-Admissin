from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    FeeViewSet,
    OrderViewSet,
    PaymentViewSet,
    InitiatePaymentView,
    PaymentCheckView,
    PaymentRedirectView
)

router = DefaultRouter()
router.register(r"fees", FeeViewSet, basename="fee")
router.register(r"orders", OrderViewSet, basename="order")
router.register(r"payments", PaymentViewSet, basename="payment")

urlpatterns = [
    path("", include(router.urls)),
    path("initiate/", InitiatePaymentView.as_view(), name="initiate-payment"),
    path(
        "check/<uuid:order_id>/", PaymentCheckView.as_view(), name="payment-check"
    ),  # ✅ دي جديدة
    path("redirect/<uuid:order_id>/", PaymentRedirectView.as_view()),

]
