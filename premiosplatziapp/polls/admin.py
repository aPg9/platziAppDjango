from django.contrib import admin
from .models import Choice, Question


class ChoiceInLine(admin.StackedInline):
    model = Choice
    extra = 3

class QuestionAdmin(admin.ModelAdmin):
    fields = ["pub_date", "question_text"]
    inlines = [ChoiceInLine]

admin.site.register(Question, QuestionAdmin)
