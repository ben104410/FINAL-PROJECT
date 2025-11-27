from django.db import models
from django.conf import settings


class Quiz(models.Model):
    course = models.ForeignKey('courses.Course', on_delete=models.CASCADE, related_name="quizzes")
    title = models.CharField(max_length=255)
    instructions = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title


class Question(models.Model):
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE, related_name="questions")
    text = models.CharField(max_length=500)

    def __str__(self):
        return self.text


class Choice(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name="choices")
    text = models.CharField(max_length=300)
    is_correct = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.text} ({'correct' if self.is_correct else 'wrong'})"


class QuizAttempt(models.Model):
    student = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="quiz_attempts")
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE)
    score = models.IntegerField(default=0)
    taken_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.student.username} - {self.quiz.title} ({self.score})"


class SelectedAnswer(models.Model):
    attempt = models.ForeignKey(QuizAttempt, on_delete=models.CASCADE, related_name="answers")
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    choice = models.ForeignKey(Choice, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.question.text} -> {self.choice.text}"

# Create your models here.
