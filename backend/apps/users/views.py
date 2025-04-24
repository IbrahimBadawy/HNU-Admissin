from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from .models import Program
from .serializers import *
from .permissions import *


class ProgramViewSet(viewsets.ModelViewSet):
    queryset = Program.objects.all()
    serializer_class = ProgramSerializer
    permission_classes = [IsAuthenticated, HasUserPageRolePermission]

    def get_queryset(self):
        if self.request.user.is_superuser:
            return Program.objects.all()
        allowed_programs = get_user_allowed_programs(self.request.user)
        return Program.objects.filter(id__in=allowed_programs)

    def get_permissions(self):
        if self.action in ["retrieve", "update", "partial_update", "destroy"]:
            return [
                IsAuthenticated(),
                HasUserPageRolePermission(),
                HasUserDataAccessPermission(),
            ]
        return super().get_permissions()


class FacultyViewSet(viewsets.ModelViewSet):
    queryset = Faculty.objects.all()
    serializer_class = FacultySerializer
    permission_classes = [IsAuthenticated, HasUserPageRolePermission]

    def get_queryset(self):
        if self.request.user.is_superuser:
            return Faculty.objects.all()
        allowed_programs = get_user_allowed_programs(self.request.user)
        return Faculty.objects.filter(program__id__in=allowed_programs).distinct()


class UniversityViewSet(viewsets.ModelViewSet):
    queryset = University.objects.all()
    serializer_class = UniversitySerializer
    permission_classes = [IsAuthenticated, HasUserPageRolePermission]

    def get_queryset(self):
        if self.request.user.is_superuser:
            return University.objects.all()
        allowed_programs = get_user_allowed_programs(self.request.user)
        return University.objects.filter(
            faculty__program__id__in=allowed_programs
        ).distinct()
