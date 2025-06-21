from rest_framework import serializers
from .models import Program, Faculty, University,AcademicYear


class UniversitySerializer(serializers.ModelSerializer):
    class Meta:
        model = University
        fields = ["id", "name"]


class FacultySerializer(serializers.ModelSerializer):
    university = UniversitySerializer(read_only=True)

    class Meta:
        model = Faculty
        fields = ["id", "name", "university"]


class ProgramSerializer(serializers.ModelSerializer):
    faculty = serializers.PrimaryKeyRelatedField(queryset=Faculty.objects.all())
    sis_code = serializers.CharField(required=False)

    class Meta:
        model = Program
        fields = ["id", "name", "faculty",'sis_code']

class AcademicYearSerializer(serializers.ModelSerializer):
    class Meta:
        model = AcademicYear
        fields = "__all__"