from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated
from drf_spectacular.utils import extend_schema
from .models import Question, Answer
from .serializers import QuestionSerializer, SubmitExamSerializer
from .docs import question_parameters,submit_exam_response


@extend_schema(
        summary="Filter questions by tag",
        parameters=question_parameters,
        responses=QuestionSerializer(many=True),
    )
class QuestionListView(generics.ListAPIView):

    serializer_class = QuestionSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        tag = self.request.query_params.get("tag")
        if tag:
            return Question.objects.filter(tag__name=tag)
        return Question.objects.none()




# class SubmitExamView(APIView):
#     permission_classes = [IsAuthenticated]
#     @extend_schema(
#         summary="submit exam answer",
#         request=SubmitExamSerializer,
#         responses=submit_exam_response,
#         description="Returns User's Score. (correct_answers/total_question)*100"
#     )

#     def post(self, request):
#         # """
#         # Expected request body:
#         # {
#         #     "tag_name": "test1",
#         #     "answers": [
#         #         {"question": 1, "answer": 3},
#         #         {"question": 2, "answer": 8}
#         #     ]
#         # }
#         # """
#         tag = request.data.get("tag_name")
#         user_answers = request.data.get("answers", [])

#         total_questions = Question.objects.filter(tag__name=tag).count()
#         correct_count = 0

#         for ua in user_answers:
#             try:
#                 # question = Question.objects.get(id=ua["question"], tag=tag)
#                 answer = Answer.objects.get(id=ua["answer_id"], question_id=ua["question_id"])
#                 if answer.is_correct:
#                     correct_count += 1
#             except (Question.DoesNotExist, Answer.DoesNotExist):
#                 continue

#         score = (correct_count / total_questions) * 100 if total_questions > 0 else 0

#         return Response({
#             "tag": tag,
#             "total_questions": total_questions,
#             "correct_answers": correct_count,
#             "score_percent": score
#         }, status=status.HTTP_200_OK)


@extend_schema(
        summary="submit exam answer",
        request=SubmitExamSerializer,
        responses=submit_exam_response,
        description="Returns User's Score. (correct_answers/total_question)*100"
    )
class SubmitExamView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = SubmitExamSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        answers = serializer.validated_data["answers"]
        tag = serializer.validated_data["tag"]
        total_questions = Question.objects.filter(tag__name=tag).count()

        correct_count = 0
        for ans in answers:
            try:
                answer = Answer.objects.get(id=ans["answer_id"], question=ans["question_id"])
                if answer.is_correct:
                    correct_count  += 1
            except Answer.DoesNotExist:
                continue
        score = (correct_count / total_questions) * 100 if total_questions > 0 else 0

        return Response({
            "tag": tag,
            "total_questions": total_questions,
            "correct_answers": correct_count,
            "score_percent": score
        }, status=status.HTTP_200_OK)