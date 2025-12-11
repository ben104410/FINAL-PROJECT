from django.db import models
from django.conf import settings

class Comment(models.Model):
    course = models.ForeignKey('courses.Course', on_delete=models.CASCADE, related_name="comments")
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username}: {self.text[:30]}"

# Create your models here.
