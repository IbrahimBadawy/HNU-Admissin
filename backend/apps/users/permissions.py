from rest_framework.permissions import BasePermission
from .models import *


class HasUserPageRolePermission(BasePermission):
    """
    صلاحية التحقق من إمكانية دخول المستخدم إلى صفحة معينة بناءً على دوره
    """

    def has_permission(self, request, view):
        if request.user.is_superuser:
            return True

        route = request.path.replace("/api/", "/")
        print(route)
        return UserPageRole.objects.filter(
            user=request.user,
            page__path=route,
            page__type="api",
        ).exists()


class HasUserDataAccessPermission(BasePermission):
    """
    صلاحية التحقق من إمكانية رؤية بيانات البرنامج بحسب الصلاحية الهرمية للمستخدم
    تستخدم في views التي تعرض بيانات تتبع برامج
    """

    def has_object_permission(self, request, view, obj):
        if request.user.is_superuser:
            return True

        if hasattr(obj, "program_id"):
            allowed_program_ids = get_user_allowed_programs(request.user)
            return obj.program_id in allowed_program_ids

        return False


# مكررة هنا مؤقتًا للاستخدام من داخل permission، يُفضل نقلها لـ utils.py واستيرادها


def get_user_allowed_programs(user):
    access = UserDataAccess.objects.filter(user=user).select_related(
        "university", "faculty", "program"
    )
    program_ids = set()

    for a in access:
        if a.university and not a.faculty:
            programs = Program.objects.filter(
                faculty__university=a.university
            ).values_list("id", flat=True)
        elif a.university and a.faculty and not a.program:
            programs = Program.objects.filter(
                faculty=a.faculty, faculty__university=a.university
            ).values_list("id", flat=True)
        elif a.university and a.faculty and a.program:
            programs = [a.program.id]
        else:
            programs = []

        program_ids.update(programs)
    print(list(program_ids))
    return list(program_ids)
