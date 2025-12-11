from django.urls import path
from .views import UserActivityView

urlpatterns = [
    path('', UserActivityView.as_view(), name="user-activity"),
]