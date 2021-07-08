from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from django.views import generic

from .models import Survey, Answer, AnswerSet, AnswerSubset


@login_required
def index(request):
    survey_list = Survey.objects.filter(created_by=request.user)
    if request.user.is_superuser:
        survey_list = Survey.objects.all()
    context = {'survey_list': survey_list, 'user': request.user}
    return render(request, 'survey/index.html', context)


class IndexView(generic.ListView):
    template_name = 'survey/index.html'

    def get_queryset(self):
        if self.request.user.is_superuser:
            return Survey.objects.all()
        else:
            return Survey.objects.filter(created_by=self.request.user)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        survey_list = Survey.objects.filter(created_by=self.request.user)
        if self.request.user.is_superuser:
            survey_list = Survey.objects.all()

        context['survey_list'] = survey_list
        context['user'] = self.request.user

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
