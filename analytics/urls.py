from django.urls import path
from .views import (
    StudentPerformanceView,
    CoursePopularityView,
    QuizScoreDistributionView,
    CourseProgressView
)

urlpatterns = [
    path('student-performance/', StudentPerformanceView.as_view(), name="student-performance"),
    path('course-popularity/', CoursePopularityView.as_view(), name="course-popularity"),
    path('quiz-scores/<int:quiz_id>/', QuizScoreDistributionView.as_view(), name="quiz-score-distribution"),
    path('course-progress/', CourseProgressView.as_view(), name="course-progress"),
]
