from django.contrib import admin
from .models import Question, Choice, QuizRecord

class ChoiceInline(admin.TabularInline):
    model = Choice
    extra = 4

@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    inlines = [ChoiceInline]
    list_display = ('text',)

@admin.register(QuizRecord)
class QuizRecordAdmin(admin.ModelAdmin):
    list_display = ('created_at', 'duration_seconds')
    filter_horizontal = ('wrong_questions',)