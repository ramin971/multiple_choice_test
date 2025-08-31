from django.db import models


class Question(models.Model):
    text = models.CharField(max_length=255)
    tag = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.text} ({self.tag})"


class Answer(models.Model):
    question = models.ForeignKey(Question, related_name="answers", on_delete=models.CASCADE)
    text = models.CharField(max_length=255)
    is_correct = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.text} (Correct: {self.is_correct})"
