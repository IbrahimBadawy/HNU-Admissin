from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ProgramViewSet, FacultyViewSet, UniversityViewSet

router = DefaultRouter()
router.register(r"programs", ProgramViewSet, basename="program")
router.register(r"faculties", FacultyViewSet, basename="faculty")
router.register(r"universities", UniversityViewSet, basename="university")

urlpatterns = [
    path("", include(router.urls)),
]
