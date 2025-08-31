from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import generics, status
from .models import Question, Answer
from .serializers import QuestionSerializer


# list questions by tag
class QuestionListView(generics.ListAPIView):
    serializer_class = QuestionSerializer

    def get_queryset(self):
        tag = self.request.query_params.get("tag")
        if tag:
            return Question.objects.filter(tag=tag)
        return Question.objects.none()


#  submit answers & calculate score
class SubmitExamView(APIView):
    def post(self, request):
        """
        Expected request body:
        {
            "tag": "test1",
            "answers": [
                {"question": 1, "answer": 3},
                {"question": 2, "answer": 8}
            ]
        }
        """
        tag = request.data.get("tag")
        user_answers = request.data.get("answers", [])

        questions = Question.objects.filter(tag=tag).prefetch_related("answers")
        total_questions = questions.count()
        correct_count = 0

        for ua in user_answers:
            try:
                question = Question.objects.get(id=ua["question"], tag=tag)
                answer = Answer.objects.get(id=ua["answer"], question=question)
                if answer.is_correct:
                    correct_count += 1
            except (Question.DoesNotExist, Answer.DoesNotExist):
                continue

        score = (correct_count / total_questions) * 100 if total_questions > 0 else 0

        return Response({
            "tag": tag,
            "total_questions": total_questions,
            "correct_answers": correct_count,
            "score_percent": score
        }, status=status.HTTP_200_OK)
