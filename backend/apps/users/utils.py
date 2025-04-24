# users/utils.py
from .models import *


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
