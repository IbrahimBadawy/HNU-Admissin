from django.contrib import admin
from .models import *


# Register your models here.
@admin.register(University)
class UniversityAdmin(admin.ModelAdmin):
    list_display = ("id", "name")


admin.site.register(Profile)


@admin.register(Faculty)
class FacultyAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "university")
    list_filter = ("university",)


@admin.register(Program)
class ProgramAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "faculty","sis_code")
    list_filter = ("faculty__university", "faculty")
    ordering = ("sis_code",)



@admin.register(Role)
class RoleAdmin(admin.ModelAdmin):
    list_display = ("id", "name")


@admin.register(Page)
class PageAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "path", "type")
    list_filter = ("type",)


@admin.register(UserPageRole)
class UserPageRoleAdmin(admin.ModelAdmin):
    list_display = ("user", "page", "role")
    list_filter = ("role", "page__type")
    search_fields = ("user__username",)


@admin.register(UserDataAccess)
class UserDataAccessAdmin(admin.ModelAdmin):
    list_display = ("user", "university", "faculty", "program")
    list_filter = ("university", "faculty", "program")
    search_fields = ("user__username",)

@admin.register(AcademicYear)
class AcademicYearAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "start_date", "end_date","sis_add")