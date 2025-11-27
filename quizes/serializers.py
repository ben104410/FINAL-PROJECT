from rest_framework import serializers
from .models import Quiz, Question, Choice, QuizAttempt, SelectedAnswer


class ChoiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Choice
        fields = ['id', 'text', 'is_correct']


class QuestionSerializer(serializers.ModelSerializer):
    choices = ChoiceSerializer(many=True)

    class Meta:
        model = Question
        fields = ['id', 'text', 'choices']


class QuizSerializer(serializers.ModelSerializer):
    questions = QuestionSerializer(many=True)

    class Meta:
        model = Quiz
        fields = ['id', 'title', 'instructions', 'created_at', 'questions']


class QuizAttemptSerializer(serializers.ModelSerializer):
    class Meta:
        model = QuizAttempt
        fields = ['id', 'quiz', 'score', 'taken_at']
