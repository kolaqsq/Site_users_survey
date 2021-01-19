from django.contrib import admin
from django.contrib.admin import DateFieldListFilter
from django.core.exceptions import ValidationError

from .models import Survey, Section, Question, OptionGroup, OptionChoice, QuestionType


def make_open(modeladmin, request, queryset):
    queryset.update(is_open=True)


make_open.short_description = 'Сделать доступными для заполнения'


def make_close(modeladmin, request, queryset):
    queryset.update(is_open=False)


make_close.short_description = 'Сделать недоступными для заполнения'


class SectionInline(admin.StackedInline):
    model = Section
    extra = 1


class SurveyAdmin(admin.ModelAdmin):
    inlines = [SectionInline]
    actions = [make_open, make_close]

    def get_list_display(self, request):
        if request.user.is_superuser:
            return ['creator', 'survey_title', 'is_open', 'creation_date']
        else:
            return ['survey_title', 'is_open', 'creation_date']

    def get_list_filter(self, request):
        if request.user.is_superuser:
            return ['creator', 'is_open', ('creation_date', DateFieldListFilter)]
        else:
            return ['is_open', ('creation_date', DateFieldListFilter)]

    def get_queryset(self, request):
        query = Survey.objects.filter(creator=request.user)
        if request.user.is_superuser:
            query = Survey.objects.all()
        return query

    def save_model(self, request, obj, formset, change):
        obj.creator = request.user
        super().save_model(request, obj, formset, change)

    def save_related(self, request, form, formsets, change):
        for f in formsets:
            for obj in f:
                obj.instance.creator = request.user
        super(SurveyAdmin, self).save_related(request, form, formsets, change)


class QuestionInline(admin.StackedInline):
    model = Question
    extra = 1


class SectionAdmin(admin.ModelAdmin):
    inlines = [QuestionInline]

    def get_list_display(self, request):
        if request.user.is_superuser:
            return ['creator', 'survey', 'section_title']
        else:
            return ['survey', 'section_title']

    def get_list_filter(self, request):
        if request.user.is_superuser:
            return ['creator', 'survey']
        else:
            return ['survey']

    def get_queryset(self, request):
        query = Section.objects.filter(creator=request.user)
        if request.user.is_superuser:
            query = Section.objects.all()
        return query

    def save_model(self, request, obj, form, change):
        obj.creator = request.user
        current_user = Survey.objects.filter(creator=request.user)
        chosen_user = Survey.objects.filter(creator=obj.survey.creator)
        if list(current_user) == list(chosen_user):
            super().save_model(request, obj, form, change)
        else:
            raise ValidationError('Вы не можете изменять данную акету')


class OptionChoiceInline(admin.StackedInline):
    model = OptionChoice
    extra = 1


class OptionGroupAdmin(admin.ModelAdmin):
    inlines = [OptionChoiceInline]

    def get_list_display(self, request):
        if request.user.is_superuser:
            return ['creator', 'group_name']
        else:
            return ['group_name']

    def get_list_filter(self, request):
        if request.user.is_superuser:
            return []
        else:
            return ['creator']

    def get_queryset(self, request):
        query = OptionGroup.objects.filter(creator=request.user)
        if request.user.is_superuser:
            query = OptionGroup.objects.all()
        return query

    def save_model(self, request, obj, form, change):
        obj.creator = request.user
        super().save_model(request, obj, form, change)


admin.site.register(Survey, SurveyAdmin)
admin.site.register(Section, SectionAdmin)
admin.site.register(OptionGroup, OptionGroupAdmin)
admin.site.register(QuestionType)
