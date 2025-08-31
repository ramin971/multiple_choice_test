from django.urls import path
from .views import QuestionListView, SubmitExamView

urlpatterns = [
    path("questions/", QuestionListView.as_view(), name="question-list"),
    path("submit/", SubmitExamView.as_view(), name="submit-exam"),
]
