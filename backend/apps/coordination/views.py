# ✅ optimized_views_serializers.py

from django.db.models import Count, Prefetch
from rest_framework import viewsets, status, filters
from rest_framework.viewsets import ReadOnlyModelViewSet
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import PermissionDenied
from django_filters.rest_framework import DjangoFilterBackend
from django.core.files.storage import default_storage
from django.db.models import Count,OuterRef, Exists, Q
from django.db.models import OuterRef, Subquery


from .models import AcademicYear,ProgramFee
from .serializers import (
    AcademicYearSerializer,
    ProgramFeeSerializer,

)


# Create your views here.
# coordination/views.py
class AcademicYearViewSet(viewsets.ModelViewSet):
    queryset = AcademicYear.objects.all()
    serializer_class = AcademicYearSerializer
    # permission_classes = [IsAuthenticated]

class ProgramFeeViewSet(viewsets.ModelViewSet):
    queryset = ProgramFee.objects.all()
    serializer_class = ProgramFeeSerializer
    # permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend]  # ← فعل الفلترة هنا
    filterset_fields = ['academic_year', 'program']  # ← دول الفلاتر المسموح بيها
