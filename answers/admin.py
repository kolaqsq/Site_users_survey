from django.contrib import admin
from django.contrib.admin import DateFieldListFilter
from django.db import connection

from answers.models import Surveyee, SurveyeeSurvey, QuestionOption, Answer
from surveys.models import Survey


class AnswerInline(admin.StackedInline):
    model = Answer
    extra = 0


class SurveyeeSurveyAdmin(admin.ModelAdmin):
    inlines = [AnswerInline]

    def get_list_display(self, request):
        if request.user.is_superuser:
            return ['creator', 'survey_title', 'name', 'surname']
        else:
            return ['survey_title', 'name', 'surname']

    def get_list_filter(self, request):
        if request.user.is_superuser:
            return ['creator', 'survey']
        else:
            return ['survey']

    def get_queryset(self, request):
        query = SurveyeeSurvey.objects.filter(creator=request.user)
        if request.user.is_superuser:
            query = SurveyeeSurvey.objects.all()
        return query

    def survey_title(self, obj):
        return obj.survey.survey_title

    survey_title.short_description = 'Анкета'

    def name(self, obj):
        return obj.surveyee.name

    name.short_description = 'Имя'

    def surname(self, obj):
        return obj.surveyee.surname

    surname.short_description = 'Фамилия'


class SurveyeeAdmin(admin.ModelAdmin):
    list_display = ['name', 'surname']
    list_filter = ['name', 'surname']
    search_fields = ['name', 'surname']


admin.site.register(Surveyee, SurveyeeAdmin)
admin.site.register(SurveyeeSurvey, SurveyeeSurveyAdmin)
