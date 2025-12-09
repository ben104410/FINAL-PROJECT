from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.apps import apps


# 1. Student performance analytics
class StudentPerformanceView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        QuizAttempt = apps.get_model('quizes', 'QuizAttempt')  # lazy lookup
        attempts = QuizAttempt.objects.filter(student=request.user).order_by('taken_at')

        data = [{
            "quiz": attempt.quiz.title,
            "score": attempt.score,
            "date": attempt.taken_at
        } for attempt in attempts]

        return Response({"performance": data})


# 2. Course popularity (top enrolled courses)
class CoursePopularityView(APIView):
    def get(self, request):
        Course = apps.get_model('courses', 'Course')
        Enrollment = apps.get_model('courses', 'Enrollment')

        courses = Course.objects.all()

        data = []
        for c in courses:
            count = Enrollment.objects.filter(course=c).count()
            data.append({
                "course": c.title,
                "enrollments": count
            })

        return Response({"popularity": data})


# 3. Quiz score distribution for instructors
class QuizScoreDistributionView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, quiz_id):
        QuizAttempt = apps.get_model('quizes', 'QuizAttempt')
        attempts = QuizAttempt.objects.filter(quiz_id=quiz_id)

        data = [{
            "student": a.student.username,
            "score": a.score
        } for a in attempts]

        return Response({"scores": data})


# 4. Student progress in each course
class CourseProgressView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        Enrollment = apps.get_model('courses', 'Enrollment')
        QuizAttempt = apps.get_model('quizes', 'QuizAttempt')

        enrollments = Enrollment.objects.filter(student=request.user)

        data = []
        for e in enrollments:
            attempts = QuizAttempt.objects.filter(quiz__course=e.course, student=request.user)
            total_quizzes = e.course.quizzes.count()

            progress = 0
            if total_quizzes > 0:
                progress = round((attempts.count() / total_quizzes) * 100)

            data.append({
                "course": e.course.title,
                "progress": progress
            })

        return Response({"progress": data})

# Create your views here.
