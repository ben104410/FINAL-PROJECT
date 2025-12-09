from rest_framework import generics, permissions, status
from rest_framework.response import Response
from django.apps import apps

class NotificationListView(generics.ListAPIView):
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        Notification = apps.get_model('notifications', 'Notification')
        return Notification.objects.filter(user=self.request.user).order_by('-created_at')

    def get_serializer_class(self):
        from .serializers import NotificationSerializer
        return NotificationSerializer


class MarkNotificationReadView(generics.UpdateAPIView):
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        Notification = apps.get_model('notifications', 'Notification')
        return Notification.objects.filter(user=self.request.user)

    def get_serializer_class(self):
        from .serializers import NotificationSerializer
        return NotificationSerializer

    def perform_update(self, serializer):
        # Mark as read and save
        serializer.instance.is_read = True
        serializer.save()
