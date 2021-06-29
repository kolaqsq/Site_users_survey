from django.contrib import admin
from django.contrib.admin import DateFieldListFilter
import nested_admin

from .models import Survey, Section, Question, QuestionType, Answer, AnswerSubset, AnswerSet


class QuestionTypeAdmin(admin.ModelAdmin):
    list_display_links = ['name', ]
    fields = ['name', 'desc', ]
    list_display = ['name', ]
    search_fields = ['name', ]


class QuestionInline(nested_admin.NestedStackedInline):
    date_hierarchy = 'created_at'
    list_display_links = ['title', ]
    empty_value_display = 'автоматическая генерация'
    fields = ['title', 'type', 'question', 'choices', 'created_at', 'updated_at', ]
    readonly_fields = ['created_at', 'updated_at', ]
    model = Question
    extra = 0
    show_change_link = True


class SectionInline(nested_admin.NestedStackedInline):
    date_hierarchy = 'created_at'
    list_display_links = ['title', ]
    empty_value_display = 'автоматическая генерация'
    fields = ['title', 'desc', 'created_at', 'updated_at', ]
    readonly_fields = ['created_at', 'updated_at', ]
    model = Section
    extra = 0
    show_change_link = True
    inlines = [QuestionInline]


class SurveyAdmin(nested_admin.NestedModelAdmin):
    date_hierarchy = 'updated_at'
    list_display_links = ['title', ]
    empty_value_display = 'автоматическая генерация'
    inlines = [SectionInline]

    def get_readonly_fields(self, request, obj=None):
        if request.user.is_superuser:
            return ['created_by', 'created_at', 'updated_at', ]
        else:
            return ['created_at', 'updated_at', ]

    def get_fields(self, request, obj=None):
        if request.user.is_superuser:
            return ['created_by', 'title', 'desc', 'is_open', 'created_at', 'updated_at', ]
        else:
            return ['title', 'desc', 'is_open', 'created_at', 'updated_at', ]

    def get_list_display(self, request):
        if request.user.is_superuser:
            return ['created_by', 'title', 'is_open', 'created_at', 'updated_at', ]
        else:
            return ['title', 'is_open', 'created_at', 'updated_at', ]

    def get_list_filter(self, request):
        if request.user.is_superuser:
            return ['created_by', 'is_open', ('created_at', DateFieldListFilter), ('updated_at', DateFieldListFilter)]
        else:
            return ['is_open', ('created_at', DateFieldListFilter), ('updated_at', DateFieldListFilter)]

    def get_search_fields(self, request):
        if request.user.is_superuser:
            return ['created_by__username', 'title', ]
        else:
            return ['title', ]

    def get_queryset(self, request):
        query = Survey.objects.filter(created_by=request.user)
        if request.user.is_superuser:
            query = Survey.objects.all()
        return query

    def save_model(self, request, obj, formset, change):
        obj.created_by = request.user
        super().save_model(request, obj, formset, change)


# class AnswerInline(nested_admin.NestedStackedInline):
#     empty_value_display = 'автоматическая генерация'
#     fields = ['question__question', 'question__choices', 'answer', 'created_at', ]
#     readonly_fields = ['created_at', ]
#     model = Answer
#     extra = 0
#     show_change_link = True
#
#
# class AnswerSubsetInline(nested_admin.NestedStackedInline):
#     empty_value_display = 'автоматическая генерация'
#     fields = ['section__desc', 'created_at', ]
#     readonly_fields = ['section__desc', 'created_at', ]
#     model = AnswerSubset
#     extra = 0
#     show_change_link = True
#     inlines = [AnswerInline]
#
#
# class AnswerSetAdmin(nested_admin.NestedModelAdmin):
#     date_hierarchy = 'created_at'
#     list_display = ['__str__', 'survey', 'created_at', ]
#     list_display_links = ['__str__', ]
#     fields = ['survey__created_by', 'survey__title', ]
#     readonly_fields = ['survey__created_by', 'survey__title', ]
#     empty_value_display = 'автоматическая генерация'

    # inlines = [AnswerSubsetInline]

    # def get_readonly_fields(self, request, obj=None):
    #     if request.user.is_superuser:
    #         return ['survey__created_by', 'created_at', ]
    #     else:
    #         return ['created_at', ]
    #
    # def get_fields(self, request, obj=None):
    #     if request.user.is_superuser:
    #         return ['survey__created_by', 'survey__title', 'survey__desc', 'created_at', ]
    #     else:
    #         return ['survey__title', 'survey__desc', 'created_at', ]
    #
    # def get_list_display(self, request):
    #     if request.user.is_superuser:
    #         return ['survey__created_by', model_str, 'survey__title', 'created_at', ]
    #     else:
    #         return [model_str, 'survey__title', 'created_at', ]
    #
    # def get_list_filter(self, request):
    #     if request.user.is_superuser:
    #         return ['survey__created_by', 'survey__title', ('created_at', DateFieldListFilter), ]
    #     else:
    #         return ['survey__title', ('created_at', DateFieldListFilter), ]
    #
    # def get_search_fields(self, request):
    #     if request.user.is_superuser:
    #         return ['survey__created_by', 'survey__title', 'created_at', ]
    #     else:
    #         return ['survey__title', 'created_at', ]
    #
    # def get_queryset(self, request):
    #     query = AnswerSet.objects.filter(survey__created_by=request.user)
    #     if request.user.is_superuser:
    #         query = AnswerSet.objects.all()
    #     return query


admin.site.register(Survey, SurveyAdmin)
admin.site.register(QuestionType, QuestionTypeAdmin)
# admin.site.register(AnswerSet, AnswerSetAdmin)
