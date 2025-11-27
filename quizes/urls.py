from django.urls import path
from .views import (
    CreateQuizView,
    AddQuestionView,
    TakeQuizView,
    QuizAttemptsView
)

urlpatterns = [
    path('create/', CreateQuizView.as_view(), name="create-quiz"),
    path('<int:quiz_id>/add-question/', AddQuestionView.as_view(), name="add-question"),
    path('<int:quiz_id>/take/', TakeQuizView.as_view(), name="take-quiz"),
    path('attempts/', QuizAttemptsView.as_view(), name="quiz-attempts"),
]
