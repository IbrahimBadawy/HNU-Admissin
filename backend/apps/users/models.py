from django.db import models
from django.contrib.auth.models import User


# ---------------------------
# المؤسسات التعليمية
# ---------------------------
class University(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Faculty(models.Model):
    name = models.CharField(max_length=100)
    university = models.ForeignKey(University, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.name} ({self.university.name})"


class Program(models.Model):
    name = models.CharField(max_length=100)
    faculty = models.ForeignKey(Faculty, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.name} - {self.faculty.name}"


# ---------------------------
# نظام الصلاحيات
# ---------------------------
class Role(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Page(models.Model):
    name = models.CharField(max_length=100)
    path = models.CharField(max_length=200, unique=True)
    component = models.CharField(max_length=100)
    type = models.CharField(max_length=20, choices=[("route", "Route"), ("api", "API")])

    def __str__(self):
        return f"{self.name} ({self.type})"


class UserPageRole(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    page = models.ForeignKey(Page, on_delete=models.CASCADE)
    role = models.ForeignKey(Role, on_delete=models.CASCADE)

    class Meta:
        unique_together = ("user", "page")

    def __str__(self):
        return f"{self.user.username} - {self.page.name} - {self.role.name}"


class UserDataAccess(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    university = models.ForeignKey(
        University, null=True, blank=True, on_delete=models.CASCADE
    )
    faculty = models.ForeignKey(
        Faculty, null=True, blank=True, on_delete=models.CASCADE
    )
    program = models.ForeignKey(
        Program, null=True, blank=True, on_delete=models.CASCADE
    )

    class Meta:
        unique_together = ("user", "university", "faculty", "program")

    def __str__(self):
        return f"{self.user.username} - {self.university or ''} - {self.faculty or ''} - {self.program or ''}"


# ---------------------------
# فلترة البرامج المتاحة لمستخدم
# ---------------------------
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

    return list(program_ids)
