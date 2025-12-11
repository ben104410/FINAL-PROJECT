from django.urls import path
from .views import CourseCommentsView

urlpatterns = [
    path('<int:course_id>/', CourseCommentsView.as_view(), name="course-comments"),
]
