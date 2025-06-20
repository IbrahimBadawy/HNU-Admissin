from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import *

router = DefaultRouter()
router.register(r"programs", ProgramViewSet, basename="program")
router.register(r"faculties", FacultyViewSet, basename="faculty")
router.register(r"universities", UniversityViewSet, basename="university")

urlpatterns = [
    path("", include(router.urls)),
    path("signup/", SignupView.as_view(), name="signup"),
    path("user_data/", get_user, name="user_data"),
    path("set_user_password/", set_user_password, name="set_user_password"),
]
