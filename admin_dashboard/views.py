from django.db.models import Count
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response
from django.apps import apps

class AdminDashboardView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        User = apps.get_model('users', 'User')
        Course = apps.get_model('courses', 'Course')
        Enrollment = apps.get_model('courses', 'Enrollment')
        Quiz = apps.get_model('quizes', 'Quiz')

        # Only admins allowed
        if not request.user.is_superuser:
            return Response({"error": "Admin access only"}, status=403)

        # 1. User statistics
        total_users = User.objects.count()
        total_students = User.objects.filter(role="student").count()
        total_instructors = User.objects.filter(role="instructor").count()

        # 2. Course statistics
        total_courses = Course.objects.count()
        total_quizzes = Quiz.objects.count()

        # 3. Enrollment statistics
        total_enrollments = Enrollment.objects.count()

        # 4. Most popular courses
        popular_courses = (
            Course.objects.annotate(enrollments=Count("enrolled_students"))
            .order_by("-enrollments")
            .values("title", "enrollments")[:5]
        )

        # 5. Daily new user registrations
        daily_users = (
            User.objects.extra(select={'date': "date(date_joined)"})
            .values("date")
            .annotate(count=Count("id"))
            .order_by("date")
        )

        # 6. Daily course enrollments
        daily_enrollments = (
            Enrollment.objects.extra(select={'date': "date(enrolled_at)"})
            .values("date")
            .annotate(count=Count("id"))
            .order_by("date")
        )

        data = {
            "total_users": total_users,
            "total_students": total_students,
            "total_instructors": total_instructors,
            "total_courses": total_courses,
            "total_enrollments": total_enrollments,
            "total_quizzes": total_quizzes,
            "popular_courses": list(popular_courses),
            "daily_users": list(daily_users),
            "daily_enrollments": list(daily_enrollments),
        }

        return Response(data, status=200)