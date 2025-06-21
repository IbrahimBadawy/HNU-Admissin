from django.contrib import admin
from .models import *

admin.site.register(Fee)
admin.site.register(FeesTypes)
admin.site.register(FeesList)
admin.site.register(Order)
admin.site.register(Payment)

@admin.register(ProgramFee)
class ProgramFeeAdmin(admin.ModelAdmin):
    list_display = ("program", "academic_year","fee_list", "amount")
    list_filter = ("academic_year", "program")



