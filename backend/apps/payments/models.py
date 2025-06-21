import uuid
from django.db import models
from django.utils import timezone

from django.utils import timezone

class FeesTypes(models.Model):

    value = models.CharField(max_length=255, unique=True)
    title = models.CharField(max_length=255)

    def __str__(self):
        return self.title


class FeesList(models.Model):
    title = models.CharField(max_length=255)
    fees_types = models.ForeignKey(
        FeesTypes,
        related_name="fees_types",  # actual column in the DB
        on_delete=models.SET_NULL,
        null=True,
    )

    def __str__(self):
        return self.title


class ProgramFee(models.Model):
    academic_year = models.ForeignKey(
        "users.AcademicYear", related_name="fees_by_year", on_delete=models.CASCADE
    )
    program = models.ForeignKey(
        "users.Program", related_name="fees_by_program", on_delete=models.CASCADE
    )
    fee_list = models.ForeignKey(
        "payments.FeesList", related_name="fees_by_list", on_delete=models.CASCADE
    )
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    is_requierd = models.BooleanField(default=False)


class Fee(models.Model):
    submission = models.ForeignKey(
        "admissions.FormSubmission",  # 🔁 الربط باستخدام string لتجنب import loop
        on_delete=models.SET_NULL,
        related_name="fees",
        null=True,  # ← مهم
        blank=True,
    )
    description = models.CharField(
        max_length=255
    )
    fee_type = models.CharField(max_length=255, null=True, blank=True, default="initial"  )
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    is_paid = models.BooleanField(default=False)
    fees_list = models.ForeignKey(
        ProgramFee,  # 🔁 الربط باستخدام string لتجنب import loop
        on_delete=models.SET_NULL,
        related_name="fees_fees_list",
        null=True,  # ← مهم
        blank=True,
        default="95",
    )
    # 🆕 الحقول المطلوبة
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True,blank=True)
    def __str__(self):
        return f"{self.description} - {self.amount} EGP"

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["submission", "fees_list"], name="unique_submission_fee_list"
            )
        ]


class Order(models.Model):

    ORDERTYPES = [
        ("initial", "Initial"),
        ("collage", "Collage"),
    ]
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    submission = models.ForeignKey(
        "admissions.FormSubmission",
        # on_delete=models.CASCADE,
        on_delete=models.SET_NULL,
        null=True,
        related_name="orders",
    )
    order_type = models.CharField(
        max_length=20, choices=ORDERTYPES, blank=True, default="initial"
    )
    fees = models.ManyToManyField("payments.Fee", related_name="orders", blank=True)

    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)
    raw_response = models.JSONField(null=True, blank=True)

    def __str__(self):
        return f"Order {self.id}"


class Payment(models.Model):
    order = models.OneToOneField(
        Order,
        on_delete=models.SET_NULL,
        null=True,
        #  on_delete=models.CASCADE
    )
    paid_at = models.DateTimeField(default=timezone.now)
    
    status = models.CharField(max_length=50)
    details = models.JSONField(null=True, blank=True)

    def __str__(self):
        return f"Payment for Order {self.order.id}"
