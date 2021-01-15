from django.contrib import admin

from .models import Survey, Section, Question, OptionGroup, OptionChoice


class SectionInline(admin.StackedInline):
    model = Section
    extra = 1


class SurveyAdmin(admin.ModelAdmin):
    inlines = [SectionInline]


class QuestionInline(admin.StackedInline):
    model = Question
    extra = 1


class SectionAdmin(admin.ModelAdmin):
    inlines = [QuestionInline]


class OptionChoiceInline(admin.StackedInline):
    model = OptionChoice
    extra = 1


class OptionGroupAdmin(admin.ModelAdmin):
    inlines = [OptionChoiceInline]


admin.site.register(Survey, SurveyAdmin)
admin.site.register(Section, SectionAdmin)
admin.site.register(OptionGroup, OptionGroupAdmin)
