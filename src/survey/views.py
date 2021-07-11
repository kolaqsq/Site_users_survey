# from django.contrib.auth.decorators import login_required
from django.core import serializers
from django.http import HttpResponseRedirect
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.shortcuts import render
from django.urls import reverse
from django.views import generic
from django.db.models import Q

from .models import Survey, Answer, AnswerSet, AnswerSubset


class IndexView(generic.ListView):
    template_name = 'survey/index.html'

    def get_queryset(self):
        query = self.request.GET.get('q', '')

        survey_list = Survey.objects.filter(created_by=self.request.user)
        if self.request.user.is_superuser:
            survey_list = Survey.objects.all()

        if query:
            survey_list = survey_list.filter(Q(title__icontains=query) | Q(created_by__username__icontains=query))

        return survey_list

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        query = self.request.GET.get('q', '')

        survey_list = Survey.objects.filter(created_by=self.request.user)
        if self.request.user.is_superuser:
            survey_list = Survey.objects.all()

        if query:
            survey_list = survey_list.filter(Q(title__icontains=query) | Q(created_by__username__icontains=query))

        context['survey_list'] = survey_list
        context['user'] = self.request.user
        context['query'] = query

        return context


def survey(request, survey_id):
    survey_instance = get_object_or_404(Survey, pk=survey_id)

    return render(request, 'survey/survey.html', {'survey': survey_instance})


def submit(request, survey_id):
    survey_instance = get_object_or_404(Survey, pk=survey_id)
    section_list = survey_instance.section_set.all()

    answerset = AnswerSet.objects.create(survey=survey_instance)

    for section in section_list:
        answersubset = AnswerSubset.objects.create(set=answerset, section=section)
        question_list = section.question_set.all()

        for question in question_list:
            Answer.objects.create(subset=answersubset, question=question,
                                  answer=''.join(request.POST.getlist('answer_{}'.format(question.id))))

    return HttpResponseRedirect(reverse('survey:result', args=(survey_instance.id,)))


def result(request, survey_id):
    survey_instance = get_object_or_404(Survey, pk=survey_id)
    return render(request, 'survey/result.html', {'survey': survey_instance})


def dashboard_with_pivot(request):
    return render(request, 'dashboard/dashboard_with_pivot.html', {})


def pivot_data(request):
    dataset = Answer.objects.all()
    data = serializers.serialize('json', dataset)
    return JsonResponse(data, safe=False)
