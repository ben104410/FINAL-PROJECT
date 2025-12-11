from django.urls import path
from .views import InstructorStatsView

urlpatterns = [
    path('instructor/', InstructorStatsView.as_view(), name="instructor-stats"),
]
