# apps/forms/views.py

from rest_framework import viewsets, status, filters
from rest_framework.viewsets import ReadOnlyModelViewSet

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser
from django.core.files.storage import default_storage
from django.conf import settings
import os


from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated,AllowAny
from rest_framework.exceptions import PermissionDenied
from django_filters.rest_framework import DjangoFilterBackend


from .models import Form, Section, Question, Option, FormSubmission
from .serializers import FormSerializer, FormSubmissionSerializer,SubmissionListSerializer,FormListSerializer



class FormListViewSet(ReadOnlyModelViewSet):
    queryset = Form.objects.all().order_by("-created_at")
    serializer_class = FormListSerializer
    permission_classes = [IsAuthenticated]  # ✅ غيّرها لـ IsAuthenticated لو عايز
    
    
class FormViewSet(viewsets.ModelViewSet):
    queryset = Form.objects.all().order_by("-created_at")
    serializer_class = FormSerializer
    permission_classes = [IsAuthenticated]  # ✅ غيّرها لـ IsAuthenticated لو عايز

    def check_admin(self):
        """تحقق من صلاحية الأدمن."""
        if not self.request.user.is_staff:
            raise PermissionDenied("يُسمح فقط للمشرفين بتنفيذ هذا الإجراء.")

    def create(self, request, *args, **kwargs):
        self.check_admin()  # ✅ فعّل دي لو محتاج
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def update(self, request, *args, **kwargs):
        self.check_admin()  # ✅ فعّل دي لو محتاج
        partial = kwargs.pop("partial", False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response(serializer.data)

    def destroy(self, request, *args, **kwargs):
        self.check_admin()  # ✅ تأكد إنه أدمن قبل الحذف
        instance = self.get_object()

        # 🔒 منع حذف النموذج إن كان عليه أي إجابات
        if instance.submissions.exists():
            return Response(
                {"detail": "لا يمكن حذف هذا النموذج لأنه يحتوي على إجابات."},
                status=status.HTTP_400_BAD_REQUEST
            )

        self.perform_destroy(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)


# apps/forms/views.py


class FormSubmissionViewSet(viewsets.ModelViewSet):
    queryset = FormSubmission.objects.all()
    serializer_class = FormSubmissionSerializer
    
    
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ["form"]  # 🔥 فلترة مباشرة بالكويري
    search_fields = ["form"]  # 🔥 بحث مباشر في user_identifier
    

    def get_queryset(self):
        user = self.request.user
        queryset = super().get_queryset()

        if not user.is_staff:
            queryset = queryset.filter(user_identifier=user.username)

        return queryset

    def perform_create(self, serializer):
        if self.request.user.is_authenticated:
            serializer.save(user_identifier=self.request.user.username)
        else:
            serializer.save(user_identifier="guest")

    def update(self, request, *args, **kwargs):
        instance = self.get_object()

        if instance.is_locked and not request.user.is_staff:
            raise PermissionDenied(
                "You are not allowed to edit this submission. It is locked."
            )

        return super().update(request, *args, **kwargs)


class SubmissionListViewSet(ReadOnlyModelViewSet):
    queryset = FormSubmission.objects.all()
    serializer_class = SubmissionListSerializer
    
    
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ["form"]  # 🔥 فلترة مباشرة بالكويري
    search_fields = ["form"]  # 🔥 بحث مباشر في user_identifier
    

    def get_queryset(self):
        user = self.request.user
        queryset = super().get_queryset()

        if not user.is_staff:
            queryset = queryset.filter(user_identifier=user.username)

        return queryset


class FileUploadView(APIView):
    parser_classes = [MultiPartParser]
    permission_classes = [IsAuthenticated]  # إذا فيه تسجيل دخول

    def post(self, request):
        files = request.FILES.getlist('files')
        file_urls = []

        for file in files:
            path = default_storage.save(f'uploads/{file.name}', file)
            url = default_storage.url(path)  # هترجع فقط /media/uploads/filename
            file_urls.append(url)

        return Response({'urls': file_urls})