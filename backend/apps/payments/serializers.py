
from rest_framework import serializers
from .models import   Fee, Order, Payment
from django.apps import apps
from apps.admissions.models import FormSubmission
from apps.admissions.serializers import FormSubmissionSerializer  # استخدمنا Serializer من admissions


class FeeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Fee
        fields = '__all__'

class OrderSerializer(serializers.ModelSerializer):
    submission = FormSubmissionSerializer(read_only=True)

    class Meta:
        model = Order
        fields = '__all__'

class PaymentSerializer(serializers.ModelSerializer):
    order = OrderSerializer(read_only=True)

    class Meta:
        model = Payment
        fields = '__all__'