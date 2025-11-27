try:
    from django.shortcuts import render
    from rest_framework import generics, permissions
    from django.apps import apps
except Exception as e:
    # Re-raise with clearer context so import problems show up during Django startup
    raise ImportError(f"Failed to import courses.views dependencies: {e}") from e


class CourseListCreateView(generics.ListCreateAPIView):
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        Course = apps.get_model('courses', 'Course')
        return Course.objects.all()

    def get_serializer_class(self):
        from .serializers import CourseSerializer
        return CourseSerializer

    def perform_create(self, serializer):
        serializer.save(instructor=self.request.user)


class CourseDetailView(generics.RetrieveAPIView):
    permission_classes = [permissions.AllowAny]

    def get_queryset(self):
        Course = apps.get_model('courses', 'Course')
        return Course.objects.all()

    def get_serializer_class(self):
        from .serializers import CourseSerializer
        return CourseSerializer


class UploadContentView(generics.CreateAPIView):
    permission_classes = [permissions.IsAuthenticated]

    def get_serializer_class(self):
        from .serializers import CourseContentSerializer
        return CourseContentSerializer

    def perform_create(self, serializer):
        Course = apps.get_model('courses', 'Course')
        course = Course.objects.get(id=self.kwargs['course_id'])
        serializer.save(course=course)


class EnrollCourseView(generics.CreateAPIView):
    permission_classes = [permissions.IsAuthenticated]

    def get_serializer_class(self):
        from .serializers import EnrollmentSerializer
        return EnrollmentSerializer

    def perform_create(self, serializer):
        Course = apps.get_model('courses', 'Course')
        course = Course.objects.get(id=self.kwargs['course_id'])
        serializer.save(student=self.request.user, course=course)
