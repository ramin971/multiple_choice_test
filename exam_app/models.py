from django.db import models


class Tag(models.Model):
    name = models.CharField(max_length=50, unique=True)
    def __str__(self):
        return self.name
    

class Question(models.Model):
    text = models.CharField(max_length=255)
    tag = models.ForeignKey(Tag, on_delete= models.CASCADE, related_name= "questions")

    def __str__(self):
        return f"{self.text} ({self.tag})"


class Answer(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name="answers")
    text = models.CharField(max_length=255)
    is_correct = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.text} (Correct: {self.is_correct})"
