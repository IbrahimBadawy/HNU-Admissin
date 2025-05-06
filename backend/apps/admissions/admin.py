from django.contrib import admin
from .models import *

admin.site.register(Form)
admin.site.register(Tab)
admin.site.register(Section)
admin.site.register(Question)
admin.site.register(Option)


admin.site.register(FormSubmission)
admin.site.register(Answer)


# Register your models here.
