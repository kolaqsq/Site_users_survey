# from django.contrib.auth.decorators import login_required
from django.contrib.auth.decorators import login_required
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
        if self.request.user.is_superuser or self.request.user.groups.filter(name='Operators'):
            survey_list = Survey.objects.all()

        if query:
            survey_list = survey_list.filter(Q(title__icontains=query) | Q(created_by__username__icontains=query))

        return survey_list

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        query = self.request.GET.get('q', '')

        survey_list = Survey.objects.filter(created_by=self.request.user)
        if self.request.user.is_superuser or self.request.user.groups.filter(name='Operators'):
            survey_list = Survey.objects.all()

        if query:
            survey_list = survey_list.filter(Q(title__icontains=query) | Q(created_by__username__icontains=query))

        context['survey_list'] = survey_list
        context['user'] = self.request.user
        context['query'] = query

        return context


class SurveyView(generic.TemplateView):
    template_name = 'survey/survey.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        survey_instance = get_object_or_404(Survey, pk=self.kwargs['survey_id'])

        context['survey'] = survey_instance

        return context


class CreateView(generic.TemplateView):
    template_name = 'survey/create.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['user'] = self.request.user
        context['types'] = QuestionType.objects.all()

        return context


class UpdateView(generic.TemplateView):
    template_name = 'survey/update.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        survey_instance = get_object_or_404(Survey, pk=self.kwargs['survey_id'])

        context['user'] = self.request.user
        context['types'] = QuestionType.objects.all()
        context['survey'] = survey_instance

        return context


class AnswerListView(generic.ListView):
    template_name = 'survey/question_list.html'

    def get_queryset(self):
        survey_instance = get_object_or_404(Survey, pk=self.kwargs['survey_id'])

        answer_list = AnswerSet.objects.filter(survey=survey_instance)

        return answer_list

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        survey_instance = get_object_or_404(Survey, pk=self.kwargs['survey_id'])

        answer_list = AnswerSet.objects.filter(survey=survey_instance)

        context['answer_list'] = answer_list
        context['user'] = self.request.user
        context['survey'] = survey_instance

        return context


class AnswerView(generic.TemplateView):
    template_name = 'survey/answer.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        survey_instance = get_object_or_404(Survey, pk=self.kwargs['survey_id'])
        answer_instance = get_object_or_404(AnswerSet, pk=self.kwargs['answer_id'])

        context['user'] = self.request.user
        context['types'] = QuestionType.objects.all()
        context['survey'] = survey_instance
        context['answerset'] = answer_instance

        return context


class DashboardView(generic.TemplateView):
    template_name = 'survey/dashboard.html'


def dashboard_with_pivot(request):
    return render(request, 'dashboard/dashboard_with_pivot.html', {})


def pivot_data(request):
    dataset = Answer.objects.all()
    data = serializers.serialize('json', dataset)
    return JsonResponse(data, safe=False)


@login_required
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

    return HttpResponseRedirect(reverse('survey:save_success', args=(survey_obj.id,)))


@login_required
def saveSuccess(request, survey_id):
    survey_instance = get_object_or_404(Survey, pk=survey_id)
    return render(request, 'survey/save_success.html', {'survey': survey_instance})


@login_required
def saveUpdate(request, survey_id):
    survey_instance = Survey.objects.filter(pk=survey_id).update(
        title=''.join(request.POST.getlist('survey-title')),
        desc=''.join(request.POST.getlist('survey-desc')),
        is_open=1 if request.POST.getlist('survey-status') else 0
    )

    survey_instance = get_object_or_404(Survey, pk=survey_id)

    section_list = {}
    delete_list = {}
    current_section = ''
    current_question = ''
    section_iter = 0
    question_iter = 0
    delete_iter = 0

    for key, value in request.POST.lists():
        structure = key.split('-')

        if 'delete' in key:
            delete_list[delete_iter] = str(key)
            delete_iter += 1

        elif structure[0] == 'section':
            if structure[1] != current_section:
                current_section = str(structure[1])
                section_iter += 1
                question_iter = 0

            if structure[2] == 'title':
                section_list[section_iter] = {}
                section_list[section_iter]['questions'] = {}
                section_list[section_iter]['title'] = ''.join(value)

                if not structure[1].isnumeric():
                    section_list[section_iter]['id'] = structure[1]

            elif structure[2] == 'desc':
                section_list[section_iter]['desc'] = ''.join(value)

            elif structure[2] == 'question':
                if structure[3] != current_question:
                    current_question = str(structure[3])
                    question_iter += 1

                if structure[4] == 'title':
                    section_list[section_iter]['questions'][question_iter] = {}
                    section_list[section_iter]['questions'][question_iter]['title'] = ''.join(value)

                    if not structure[3].isnumeric():
                        section_list[section_iter]['questions'][question_iter]['id'] = structure[3]

                elif structure[4] == 'type':
                    section_list[section_iter]['questions'][question_iter]['type'] = ''.join(value)

                elif structure[4] == 'question':
                    section_list[section_iter]['questions'][question_iter]['question'] = ''.join(value)

                elif structure[4] == 'choices':
                    section_list[section_iter]['questions'][question_iter]['choices'] = ''.join(value)

    for section_key, section_data in section_list.items():
        if 'id' in section_data:
            section = Section.objects.filter(pk=section_data['id']).update(
                title=''.join(section_data['title']),
                desc=''.join(section_data['desc']),
            )

            section = get_object_or_404(Section, pk=section_data['id'])
        else:
            section = Section.objects.create(
                survey=survey_instance,
                title=''.join(section_data['title']),
                desc=''.join(section_data['desc']),
            )

        for question_key, question_data in section_data['questions'].items():
            if 'id' in question_data:
                question = Question.objects.filter(pk=question_data['id']).update(
                    title=''.join(question_data['title']),
                    type=QuestionType.objects.get(pk=''.join(question_data['type'])),
                    question=''.join(question_data['question']),
                    choices=''.join(question_data['choices']),
                )
            else:
                question = Question.objects.create(
                    section=section,
                    title=''.join(question_data['title']),
                    type=QuestionType.objects.get(pk=''.join(question_data['type'])),
                    question=''.join(question_data['question']),
                    choices=''.join(question_data['choices']),
                )

    for key, value in delete_list.items():
        structure = value.split('-')

        if structure[0] == 'survey':
            Survey.objects.filter(pk=structure[1]).delete()
            return HttpResponseRedirect(reverse('survey:delete_success'))

        elif structure[0] == 'section' and Section.objects.filter(pk=structure[1]).exists():
            Section.objects.filter(pk=structure[1]).delete()
        elif structure[0] == 'question' and Question.objects.filter(pk=structure[1]).exists():
            Question.objects.filter(pk=structure[1]).delete()

    return HttpResponseRedirect(reverse('survey:update_success', args=(survey_instance.id,)))


@login_required
def updateSuccess(request, survey_id):
    survey_instance = get_object_or_404(Survey, pk=survey_id)
    return render(request, 'survey/update_success.html', {'survey': survey_instance})


@login_required
def deleteSuccess(request):
    return render(request, 'survey/delete_success.html')


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


