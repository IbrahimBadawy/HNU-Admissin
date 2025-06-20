from django.db import models


class Form(models.Model):
    title = models.CharField(max_length=255)
    is_active = models.BooleanField(default=False)
    meta_data = models.JSONField(default=dict, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)
    is_archived = models.BooleanField(default=False)
    syear = models.ForeignKey(
        "coordination.AcademicYear",
        default='1',
        related_name="syear",
        blank=True,
        on_delete=models.DO_NOTHING,
    )


class Tab(models.Model):
    form = models.ForeignKey(Form, related_name="tabs", on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    meta_data = models.JSONField(default=dict, blank=True)
    order = models.PositiveIntegerField(default=1)
    is_archived = models.BooleanField(default=False)


class Section(models.Model):
    tab = models.ForeignKey(Tab, related_name="sections", on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    meta_data = models.JSONField(default=dict, blank=True)
    order = models.PositiveIntegerField(default=1)
    is_archived = models.BooleanField(default=False)


class Question(models.Model):
    TEXT = "text"
    NUMBER = "number"
    TEXTAREA = "textarea"
    SELECT = "select"
    MULTISELECT = "multi-select"
    RADIO = "radio"
    CHECKBOX = "checkbox"
    DATE = "date"
    FILE = "file-upload"
    DRAGGABLE = "draggable"
    PAYMENT = "payment"

    QUESTION_TYPES = [
        (TEXT, "Text"),
        (TEXTAREA, "Textarea"),
        (SELECT, "Dropdown"),
        (RADIO, "Multiple Choice"),
        (CHECKBOX, "Checkboxes"),
        (DATE, "Date Picker"),
        (FILE, "File Upload"),
        (NUMBER, "Number"),
        (MULTISELECT, "Multi Select"),
        (DRAGGABLE, "Draggable"),
        (PAYMENT, "Payment"),
    ]

    section = models.ForeignKey(
        Section, related_name="questions", on_delete=models.CASCADE
    )
    title = models.CharField(max_length=500)
    question_type = models.CharField(max_length=20, choices=QUESTION_TYPES)
    is_required = models.BooleanField(default=False)
    order = models.PositiveIntegerField(default=1)
    configs = models.JSONField(default=dict, blank=True)
    is_archived = models.BooleanField(default=False)
    meta_data = models.JSONField(default=dict, blank=True)


class Option(models.Model):
    question = models.ForeignKey(
        Question, related_name="options", on_delete=models.CASCADE
    )
    title = models.CharField(max_length=255)
    order = models.PositiveIntegerField(default=1)
    meta_data = models.JSONField(default=dict, blank=True)
    is_archived = models.BooleanField(default=False)


class FormSubmission(models.Model):
    STATUS_CHOICES = [
        ("reviewed", "مستوفي"),
        ("pending", "تحت المراجعة"),
        ("accepted", "تم القبول"),
        ("rejected", "تم الرفض"),
        ("noted", "توجد ملاحظات"),
    ]
    form = models.ForeignKey(
        Form, related_name="submissions", on_delete=models.SET_NULL, null=True
    )
    user_identifier = models.CharField(max_length=255, null=True, blank=True)  # 🔥 New
    is_locked = models.BooleanField(default=False)  # 🔥 الحقل الجديد
    meta_data = models.JSONField(default=dict, blank=True)
    is_archived = models.BooleanField(default=False)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="pending")
    notes = models.TextField(blank=True, null=True)
    is_paied = models.BooleanField(default=False, null=True, blank=True)

    modified_at = models.DateTimeField(auto_now=True)
    submitted_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Submission #{self.id} for Form {self.form.id}"


class Answer(models.Model):
    submission = models.ForeignKey(
        FormSubmission, related_name="answers", on_delete=models.CASCADE
    )
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    answer_text = models.TextField(null=True, blank=True)
    meta_data = models.JSONField(default=dict, blank=True)


class ActiveManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(is_archived=False)
