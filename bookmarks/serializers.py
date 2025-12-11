from rest_framework import serializers
from .models import Bookmark
from django.apps import apps

class CourseMiniSerializer(serializers.ModelSerializer):
    class Meta:
        model = None  # will be set dynamically

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.Meta.model is None:
            Course = apps.get_model('courses', 'Course')
            self.Meta.model = Course

    def get_fields(self):
        return {
            'id': serializers.IntegerField(read_only=True),
            'title': serializers.CharField(),
            'category': serializers.CharField(),
            'description': serializers.CharField(),
        }


class BookmarkSerializer(serializers.ModelSerializer):
    course = CourseMiniSerializer(read_only=True)

    class Meta:
        model = Bookmark
        fields = ['id', 'course', 'created_at']
