from rest_framework import serializers
from .models import AcademicYear,ProgramFee
from rest_framework.exceptions import ValidationError


# coordination/serializers.py
class AcademicYearSerializer(serializers.ModelSerializer):
    class Meta:
        model = AcademicYear
        fields = "__all__"

class ProgramFeeSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProgramFee
        fields = "__all__"
