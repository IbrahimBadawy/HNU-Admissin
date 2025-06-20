from django.db import models

# Create your models here.
class AcademicYear(models.Model):
    name = models.CharField(max_length=20)        # مثال: "2024/2025"
    start_date = models.DateField()

    end_date = models.DateField()
    sis_add = models.CharField(blank=True) 
    def __str__(self):
        return self.name


class ProgramFee(models.Model):
    academic_year = models.ForeignKey(
        AcademicYear, related_name="fees", on_delete=models.CASCADE
    )
    program = models.ForeignKey(
        "users.Program", related_name="fees", on_delete=models.CASCADE
    )
    description = models.CharField(max_length=255)   # مصروفات دراسية، إدارية…
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    is_requierd = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.program} - {self.description} ({self.academic_year})"
