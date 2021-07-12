# from django.contrib.auth.decorators import login_required
from django.core import serializers
from django.http import HttpResponseRedirect
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.shortcuts import render
from django.urls import reverse
from django.views import generic
from django.db.models import Q

from .models import Survey, Answer, AnswerSet, AnswerSubset, QuestionType, Section, Question


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


class CreateView(generic.TemplateView):
    template_name = 'survey/create.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['user'] = self.request.user
        context['types'] = QuestionType.objects.all()

        return context


def save(request):
    survey_obj = Survey.objects.create(
        created_by=request.user,
        title=''.join(request.POST.getlist('survey-title')),
        desc=''.join(request.POST.getlist('survey-desc')),
        is_open=1 if request.POST.getlist('survey-status') else 0
    )

    section_list = {}
    current_section = 0
    current_question = 0
    section_iter = 0
    question_iter = 0

    for key, value in request.POST.lists():
        if 'question' in key:
            structure = key.split('-')
            current_section = structure[1]
            current_question = structure[3]
            break

    for key, value in request.POST.lists():
        if 'section' in key:
            structure = key.split('-')

            if structure[1] != current_section:
                current_section = structure[1]
                section_iter += 1
                question_iter = 0

            if structure[2] == 'title':
                section_list[section_iter] = {}
                section_list[section_iter]['questions'] = {}
                section_list[section_iter]['title'] = ''.join(value)

            elif structure[2] == 'desc':
                section_list[section_iter]['desc'] = ''.join(value)

            elif structure[2] == 'question':
                if structure[3] != current_question:
                    current_question = structure[3]
                    question_iter += 1

                if structure[4] == 'title':
                    section_list[section_iter]['questions'][question_iter] = {}
                    section_list[section_iter]['questions'][question_iter]['title'] = ''.join(value)

                elif structure[4] == 'type':
                    section_list[section_iter]['questions'][question_iter]['type'] = ''.join(value)

                elif structure[4] == 'question':
                    section_list[section_iter]['questions'][question_iter]['question'] = ''.join(value)

                elif structure[4] == 'choices':
                    section_list[section_iter]['questions'][question_iter]['choices'] = ''.join(value)

    for section_key, section_data in section_list.items():
        section = Section.objects.create(
            survey=survey_obj,
            title=''.join(section_data['title']),
            desc=''.join(section_data['desc']),
        )

        for question_key, question_data in section_data['questions'].items():
            question = Question.objects.create(
                section=section,
                title=''.join(question_data['title']),
                type=QuestionType.objects.get(pk=''.join(question_data['type'])),
                question=''.join(question_data['question']),
                choices=''.join(question_data['choices']),
            )

    return HttpResponseRedirect(reverse('survey:index'))


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
