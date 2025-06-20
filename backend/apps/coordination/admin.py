from django.contrib import admin
from .models import AcademicYear,ProgramFee
# Register your models here.
@admin.register(AcademicYear)
class AcademicYearAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "start_date", "end_date","sis_add")

@admin.register(ProgramFee)
class ProgramFeeAdmin(admin.ModelAdmin):
    list_display = ("program", "academic_year", "description", "amount")
    list_filter = ("academic_year", "program")
