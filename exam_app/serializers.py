from rest_framework import serializers
from .models import Question, Answer



class AnswerSubmissionSerializer(serializers.Serializer):
    question_id = serializers.IntegerField()
    answer_id = serializers.IntegerField()

    def validate(self, data):
        question_id = data["question_id"]
        answer_id = data["answer_id"]

        # ensure the answer belongs to the given question
        try:
            answer = Answer.objects.get(id=answer_id, question_id=question_id)
        except Answer.DoesNotExist:
            raise serializers.ValidationError(
                f"Answer {answer_id} does not belong to Question {question_id}."
            )

        return data


class SubmitExamSerializer(serializers.Serializer):
    answers = AnswerSubmissionSerializer(many=True)
    tag = serializers.CharField()
    

class AnswerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Answer
        fields = ["id", "text"]  # Don't expose is_correct!


class QuestionSerializer(serializers.ModelSerializer):
    answers = AnswerSerializer(many=True, read_only=True)
    tag = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = Question
        fields = ["id", "text", "tag", "answers"]
