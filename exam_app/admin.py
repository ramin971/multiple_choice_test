from django.contrib import admin
from django.forms.models import BaseInlineFormSet
from django.core.exceptions import ValidationError
from .models import Question, Answer

class AnswerInlineFormset(BaseInlineFormSet):
    def clean(self):
        super().clean()
        correct_count = sum(1 for form in self.forms
                            if form.cleaned_data.get("is_correct") and not form.cleaned_data.get("DELETE", False))
        if correct_count != 1:
            raise ValidationError("You must select exactly one correct answer.")

class AnswerInline(admin.TabularInline):
    model = Answer
    extra = 4   # show 4 empty answer fields by default
    min_num = 4 # require at least 4 answers
    max_num = 4 # enforce exactly 4 answers
    formset = AnswerInlineFormset

@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = ("id", "text", "tag")
    search_fields = ("text", "tag")
    list_filter = ("tag",)
    inlines = [AnswerInline]
