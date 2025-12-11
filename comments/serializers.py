from rest_framework import serializers
from .models import Comment

class CommentSerializer(serializers.ModelSerializer):
    username = serializers.ReadOnlyField(source='user.username')

    class Meta:
        model = Comment
        fields = ['id', 'username', 'text', 'created_at']
