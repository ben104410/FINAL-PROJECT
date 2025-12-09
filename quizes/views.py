from rest_framework import generics, permissions, status
from rest_framework.response import Response
from django.apps import apps


# Instructor: create quiz
class CreateQuizView(generics.CreateAPIView):
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        Quiz = apps.get_model('quizes', 'Quiz')
        return Quiz.objects.all()

    def get_serializer_class(self):
        from .serializers import QuizSerializer
        return QuizSerializer

    def perform_create(self, serializer):
        # save quiz
        quiz = serializer.save()
        # create notification (lazy lookup to avoid circular imports)
        Notification = apps.get_model('notifications', 'Notification')
        Notification.objects.create(
            user=quiz.course.instructor,
            message=f"New quiz '{quiz.title}' added to {quiz.course.title}"
        )


# Instructor: add questions to quiz
class AddQuestionView(generics.CreateAPIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, quiz_id):
        Quiz = apps.get_model('quizes', 'Quiz')
        Question = apps.get_model('quizes', 'Question')
        Choice = apps.get_model('quizes', 'Choice')
        Notification = apps.get_model('notifications', 'Notification')

        try:
            quiz = Quiz.objects.get(id=quiz_id)
        except Quiz.DoesNotExist:
            return Response({"detail": "Quiz not found."}, status=status.HTTP_404_NOT_FOUND)

        question_text = request.data.get("text")
        choices = request.data.get("choices", [])

        if not question_text or not isinstance(choices, list) or len(choices) == 0:
            return Response({"detail": "Provide 'text' and a non-empty 'choices' list."},
                            status=status.HTTP_400_BAD_REQUEST)

        question = Question.objects.create(quiz=quiz, text=question_text)

        for choice in choices:
            Choice.objects.create(
                question=question,
                text=choice.get("text", ""),
                is_correct=bool(choice.get("is_correct", False))
            )

        # notify enrolled students about new question
        enrollments = quiz.course.enrolled_students.all()
        for enr in enrollments:
            try:
                Notification.objects.create(
                    user=enr.student,
                    message=f"New question added to quiz '{quiz.title}' in {quiz.course.title}"
                )
            except Exception:
                pass

        return Response({"message": "Question added"}, status=status.HTTP_201_CREATED)


# Student: take quiz + auto grading
class TakeQuizView(generics.CreateAPIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, quiz_id):
        Quiz = apps.get_model('quizes', 'Quiz')
        Question = apps.get_model('quizes', 'Question')
        Choice = apps.get_model('quizes', 'Choice')
        QuizAttempt = apps.get_model('quizes', 'QuizAttempt')
        SelectedAnswer = apps.get_model('quizes', 'SelectedAnswer')
        Notification = apps.get_model('notifications', 'Notification')

        try:
            quiz = Quiz.objects.get(id=quiz_id)
        except Quiz.DoesNotExist:
            return Response({"detail": "Quiz not found."}, status=status.HTTP_404_NOT_FOUND)

        answers = request.data.get("answers", [])
        if not isinstance(answers, list) or len(answers) == 0:
            return Response({"detail": "Provide a non-empty 'answers' list."}, status=status.HTTP_400_BAD_REQUEST)

        attempt = QuizAttempt.objects.create(student=request.user, quiz=quiz)

        score = 0
        for ans in answers:
            qid = ans.get("question_id")
            cid = ans.get("choice_id")
            if qid is None or cid is None:
                continue
            try:
                question = Question.objects.get(id=qid)
                choice = Choice.objects.get(id=cid)
            except (Question.DoesNotExist, Choice.DoesNotExist):
                continue

            SelectedAnswer.objects.create(
                attempt=attempt,
                question=question,
                choice=choice
            )

            if choice.is_correct:
                score += 1

        attempt.score = score
        attempt.save()

        # notify instructor about submission (non-blocking)
        try:
            Notification.objects.create(
                user=quiz.course.instructor,
                message=f"{request.user.username} submitted quiz '{quiz.title}' and scored {score}/{quiz.questions.count()}"
            )
        except Exception:
            pass

        return Response({
            "message": "Quiz submitted",
            "score": score,
            "total_questions": quiz.questions.count()
        }, status=status.HTTP_201_CREATED)


# Student: view score history
class QuizAttemptsView(generics.ListAPIView):
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        QuizAttempt = apps.get_model('quizes', 'QuizAttempt')
        return QuizAttempt.objects.filter(student=self.request.user)

# Create your views here.
