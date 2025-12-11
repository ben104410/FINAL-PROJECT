from django.shortcuts import render
from rest_framework import generics, permissions
from django.apps import apps

class UserActivityView(generics.ListAPIView):
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        ActivityLog = apps.get_model('activity_logs', 'ActivityLog')
        return ActivityLog.objects.filter(user=self.request.user).order_by('-timestamp')

    def get_serializer_class(self):
        from .serializers import ActivityLogSerializer
        return ActivityLogSerializer


class AdminActivityLogListView(generics.ListAPIView):
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        ActivityLog = apps.get_model('activity_logs', 'ActivityLog')
        # Only admins can see all activity logs
        if not self.request.user.is_superuser:
            return ActivityLog.objects.none()
        return ActivityLog.objects.all().order_by('-timestamp')

    def get_serializer_class(self):
        from .serializers import ActivityLogSerializer
        return ActivityLogSerializer