from django.shortcuts import render
from rest_framework import generics, permissions, status
from rest_framework.response import Response
from django.apps import apps

try:
    from activity_logs.utils import log_activity
except ImportError:
    log_activity = lambda *args, **kwargs: None  # fallback no-op

# Create your views here.
class BookmarkListCreateView(generics.ListCreateAPIView):
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        Bookmark = apps.get_model('bookmarks', 'Bookmark')
        return Bookmark.objects.filter(user=self.request.user).order_by('-created_at')

    def get_serializer_class(self):
        from .serializers import BookmarkSerializer
        return BookmarkSerializer

    def perform_create(self, serializer):
        bookmark = serializer.save(user=self.request.user)
        # log activity
        log_activity(self.request.user, 'bookmark', f"Bookmarked course {bookmark.course.title}")


class RemoveBookmarkView(generics.DestroyAPIView):
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        Bookmark = apps.get_model('bookmarks', 'Bookmark')
        return Bookmark.objects.filter(user=self.request.user)

    def get_serializer_class(self):
        from .serializers import BookmarkSerializer
        return BookmarkSerializer

    def perform_destroy(self, instance):
        course_title = instance.course.title
        super().perform_destroy(instance)
        # log activity
        log_activity(self.request.user, 'bookmark_removed', f"Removed bookmark from {course_title}")
