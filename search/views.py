from rest_framework.views import APIView
from rest_framework.response import Response
from django.apps import apps

class SearchView(APIView):
    def get(self, request):
        Course = apps.get_model('courses', 'Course')
        Quiz = apps.get_model('quizes', 'Quiz')
        User = apps.get_model('users', 'User')

        query = request.GET.get("q", "").strip()

        if query == "":
            return Response({"error": "Search query cannot be empty"}, status=400)

        # Search Courses by title
        courses = Course.objects.filter(title__icontains=query)

        # Search by category
        category_courses = Course.objects.filter(category__icontains=query)

        # Search quizzes
        quizzes = Quiz.objects.filter(title__icontains=query)

        # Search instructors
        instructors = User.objects.filter(
            role="instructor",
            username__icontains=query
        )

        data = {
            "courses": [{"id": c.id, "title": c.title, "category": c.category} for c in courses],
            "category_results": [{"id": c.id, "title": c.title, "category": c.category} for c in category_courses],
            "quizzes": [{"id": q.id, "title": q.title, "course": q.course.title} for q in quizzes],
            "instructors": [{"id": i.id, "username": i.username} for i in instructors],
        }

        return Response(data, status=200)