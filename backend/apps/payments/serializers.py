
from rest_framework import serializers
from .models import  Fee, Order, Payment
from .models import  FeesTypes, FeesList,ProgramFee
                    

from django.apps import apps
from apps.admissions.models import FormSubmission
from apps.admissions.serializers import FormSubmissionSerializer  # استخدمنا Serializer من admissions



class FeeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Fee
        fields = '__all__'
        read_only_fields = ['created_at', 'modified_at']

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


class FeesTypesSerializer(serializers.ModelSerializer):
    class Meta:
        model = FeesTypes
        fields = '__all__'

class FeesListSerializer(serializers.ModelSerializer):
    fees_types = FeesTypesSerializer(read_only=True)  # ← هذا يعرض البيانات
    fees_types_id = serializers.PrimaryKeyRelatedField(
        queryset=FeesTypes.objects.all(), source='fees_types', write_only=True
    )

    class Meta:
        model = FeesList
        fields = ['id', 'title', 'fees_types', 'fees_types_id']

class ProgramFeeSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProgramFee
        fields = "__all__"