from rest_framework import serializers
from .models import Course, CourseContent, Enrollment


class CourseContentSerializer(serializers.ModelSerializer):
    class Meta:
        model = CourseContent
        fields = ['id', 'title', 'file_url', 'uploaded_at']


class CourseSerializer(serializers.ModelSerializer):
    contents = CourseContentSerializer(many=True, read_only=True)

    class Meta:
        model = Course
        fields = ['id', 'title', 'description', 'category', 'instructor', 'contents', 'created_at']
        read_only_fields = ['instructor']


class EnrollmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Enrollment
        fields = ['id', 'student', 'course', 'enrolled_at']
        read_only_fields = ['student']
