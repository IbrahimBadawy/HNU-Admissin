import uuid
from django.db import models
from django.utils import timezone

class Fee(models.Model):
    submission = models.ForeignKey(
        'admissions.FormSubmission',  # 🔁 الربط باستخدام string لتجنب import loop
        on_delete=models.CASCADE,
        related_name='fees',
        null=True,  # ← مهم
        blank=True
    )
    description = models.CharField(max_length=255)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    is_paid = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.description} - {self.amount} EGP"


class Order(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    submission = models.ForeignKey(
        'admissions.FormSubmission',
        on_delete=models.CASCADE,
        related_name='orders'
    )
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)
    raw_response = models.JSONField(null=True, blank=True)

    def __str__(self):
        return f"Order {self.id}"


class Payment(models.Model):
    order = models.OneToOneField(Order, on_delete=models.CASCADE)
    paid_at = models.DateTimeField(default=timezone.now)
    status = models.CharField(max_length=50)
    details = models.JSONField(null=True, blank=True)

    def __str__(self):
        return f"Payment for Order {self.order.id}"
