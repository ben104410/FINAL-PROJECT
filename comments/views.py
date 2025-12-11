from django.shortcuts import render
from rest_framework import generics, permissions
from django.apps import apps

class CourseCommentsView(generics.ListCreateAPIView):
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        Comment = apps.get_model('comments', 'Comment')
        return Comment.objects.filter(course_id=self.kwargs['course_id']).order_by('-created_at')

    def get_serializer_class(self):
        from .serializers import CommentSerializer
        return CommentSerializer

    def perform_create(self, serializer):
        serializer.save(user=self.request.user, course_id=self.kwargs['course_id'])

# Create your views here.
