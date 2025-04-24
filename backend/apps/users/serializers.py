from rest_framework import serializers
from .models import Program, Faculty, University


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
    faculty = FacultySerializer(read_only=True)

    class Meta:
        model = Program
        fields = ["id", "name", "faculty"]
