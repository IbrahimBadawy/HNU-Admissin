from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    AcademicYearViewSet,
    ProgramFeeViewSet,

)



# coordination/urls.py
router = DefaultRouter()
router.register(r'academic-years', AcademicYearViewSet)
router.register(r'program-fees', ProgramFeeViewSet)

urlpatterns = [
    path('', include(router.urls)),
]