from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import FormViewSet, FormSubmissionViewSet,SubmissionListViewSet,FormListViewSet,FileUploadView



router = DefaultRouter()
router.register(r"forms", FormViewSet, basename="forms")
router.register(r"forms-list", FormListViewSet, basename="forms-list")
router.register(r"submissions", FormSubmissionViewSet, basename="submissions")
router.register(r"submissions-list", SubmissionListViewSet, basename="submissions-list")

urlpatterns = [
    path("", include(router.urls)),
    path('upload/', FileUploadView.as_view(), name='file-upload'),


]
