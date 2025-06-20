
from rest_framework import serializers
from .models import   Fee, Order, Payment
from django.apps import apps


class FeeSerializer(serializers.ModelSerializer):
    is_paid = serializers.BooleanField(required=False)
    class Meta:
        model = Fee
        fields = '__all__'

class SubmissionSerializer(serializers.ModelSerializer):
    fees = FeeSerializer(many=True, read_only=True)

    class Meta:
        model = apps.get_model('admissions', 'FormSubmission')  # اسم التطبيق + الموديل
        fields = '__all__'

class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = '__all__'

class PaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = '__all__'
