from rest_framework import serializers
from .models import AnalyticsSnapshot, CoursePopularity, QuizScoreSnapshot, StudentProgress


class AnalyticsSnapshotSerializer(serializers.ModelSerializer):
    class Meta:
        model = AnalyticsSnapshot
        fields = ['id', 'name', 'data', 'created_at', 'notes']


class CoursePopularitySerializer(serializers.ModelSerializer):
    course = serializers.CharField(source='course.title', read_only=True)

    class Meta:
        model = CoursePopularity
        fields = ['id', 'course', 'enrollments', 'created_at']


class QuizScoreSnapshotSerializer(serializers.ModelSerializer):
    quiz = serializers.CharField(source='quiz.title', read_only=True)

    class Meta:
        model = QuizScoreSnapshot
        fields = ['id', 'quiz', 'average_score', 'min_score', 'max_score', 'distribution', 'created_at']


class StudentProgressSerializer(serializers.ModelSerializer):
    student = serializers.CharField(source='student.username', read_only=True)
    course = serializers.CharField(source='course.title', read_only=True)

    class Meta:
        model = StudentProgress
        fields = ['id', 'student', 'course', 'progress_percent', 'updated_at']
