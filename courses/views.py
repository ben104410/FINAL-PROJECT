try:
    from django.shortcuts import render
    from rest_framework import generics, permissions
    from .models import Course, CourseContent, Enrollment
    from .serializers import CourseSerializer, CourseContentSerializer, EnrollmentSerializer
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
        course = serializer.save(instructor=self.request.user)
        # notify the instructor that the course was created
        Notification = apps.get_model('notifications', 'Notification')
        try:
            Notification.objects.create(
                user=self.request.user,
                message=f"Your course '{course.title}' has been created"
            )
        except Exception:
            # don't block course creation if notification fails
            pass


class CourseDetailView(generics.RetrieveAPIView):
    permission_classes = [permissions.AllowAny]

    def get_queryset(self):
        Course = apps.get_model('courses', 'Course')
        return Course.objects.all()

    def get_serializer_class(self):
        from .serializers import CourseSerializer
        return CourseSerializer


class UploadContentView(generics.CreateAPIView):
    serializer_class = CourseContentSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        # instructor uploads content to a course they own
        course = Course.objects.get(id=self.kwargs['course_id'])
        content = serializer.save(course=course)

        # notify enrolled students about new content
        Notification = apps.get_model('notifications', 'Notification')
        enrollments = course.enrolled_students.all()  # Enrollment instances
        for enr in enrollments:
            try:
                Notification.objects.create(
                    user=enr.student,
                    message=f"New content '{content.title}' added to {course.title}"
                )
            except Exception:
                # keep it resilient; don't block upload if notification fails
                pass


class EnrollCourseView(generics.CreateAPIView):
    serializer_class = EnrollmentSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        course = Course.objects.get(id=self.kwargs['course_id'])
        enrollment = serializer.save(student=self.request.user, course=course)

        # notify instructor about new enrollment
        Notification = apps.get_model('notifications', 'Notification')
        try:
            Notification.objects.create(
                user=course.instructor,
                message=f"{self.request.user.username} enrolled in {course.title}"
            )
        except Exception:
            # don't block enrollment if notification creation fails
            pass
