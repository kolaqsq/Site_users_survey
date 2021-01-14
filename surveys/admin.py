from django.contrib import admin

from .models import Survey, QuestionType, Question

admin.site.register(Survey)
admin.site.register(QuestionType)
admin.site.register(Question)
