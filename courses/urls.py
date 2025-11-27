from django.urls import path
from .views import (
    CourseListCreateView,
    CourseDetailView,
    UploadContentView,
    EnrollCourseView
)

urlpatterns = [
    path('', CourseListCreateView.as_view(), name="courses"),
    path('<int:pk>/', CourseDetailView.as_view(), name="course-detail"),
    path('<int:course_id>/upload/', UploadContentView.as_view(), name="upload-content"),
    path('<int:course_id>/enroll/', EnrollCourseView.as_view(), name="enroll-course"),
]
