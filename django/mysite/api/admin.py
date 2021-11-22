from django.contrib import admin

from .models import Survey, Question, Choice, QuestionAnswers, QuestionChoiceAnswers

class ChoiceInline(admin.TabularInline):
    model = Choice
    extra = 1


class QuestionAdmin(admin.ModelAdmin):
    fieldsets = [
        (None,               {'fields': ['survey', 'multiple_choice', 'question_text']}),
        ('Date information', {'fields': ['pub_date'], 'classes': ['collapse']}),
    ]
    inlines = [ChoiceInline]

class SurveyAdmin(admin.ModelAdmin):
    def get_readonly_fields(self, request, obj=None):
        if obj:
            return ['start_date']
        else:
            return []

admin.site.register(Survey, SurveyAdmin)
admin.site.register(Question, QuestionAdmin)
admin.site.register(QuestionAnswers)
admin.site.register(QuestionChoiceAnswers)
