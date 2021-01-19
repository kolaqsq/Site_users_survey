from django.contrib import admin

from .models import Survey, Section, Question, OptionGroup, OptionChoice, QuestionType


class SectionInline(admin.StackedInline):
    model = Section
    extra = 1


class SurveyAdmin(admin.ModelAdmin):
    inlines = [SectionInline]

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
            for ob in f:
                ob.instance.creator = request.user
        super(SurveyAdmin, self).save_related(request, form, formsets, change)


class QuestionInline(admin.StackedInline):
    model = Question
    extra = 1


class SectionAdmin(admin.ModelAdmin):
    inlines = [QuestionInline]

    def get_queryset(self, request):
        query = Section.objects.filter(creator=request.user)
        if request.user.is_superuser:
            query = Section.objects.all()
        return query

    def save_model(self, request, obj, form, change):
        obj.creator = request.user
        super().save_model(request, obj, form, change)


class OptionChoiceInline(admin.StackedInline):
    model = OptionChoice
    extra = 1


class OptionGroupAdmin(admin.ModelAdmin):
    inlines = [OptionChoiceInline]

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
