from django.contrib.auth.models import User
from django.db import models

from surveys.models import Survey, Question, OptionChoice


class Surveyee(models.Model):
    name = models.CharField('Имя', max_length=100)
    surname = models.CharField('Фамилия', max_length=100)
    email = models.CharField('E-mail', max_length=100)

    def __str__(self):
        template = '{0.name} {0.surname}'
        return template.format(self)

    class Meta:
        verbose_name = 'Анкетируемый'
        verbose_name_plural = 'Анкетируемые'


class SurveyeeSurvey(models.Model):
    creator = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Создатель', editable=False)
    survey = models.ForeignKey(Survey, on_delete=models.CASCADE, verbose_name='Анкета')
    surveyee = models.ForeignKey(Surveyee, on_delete=models.CASCADE, verbose_name='Анкетируемый')

    def __str__(self):
        template = 'Набор ответов №{0.id}. {0.surveyee}, {0.survey}'
        return template.format(self)

    class Meta:
        verbose_name = 'Набор ответов'
        verbose_name_plural = 'Наборы ответов'


class QuestionOption(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE, verbose_name='Вопрос')
    option_choice = models.ForeignKey(OptionChoice, on_delete=models.CASCADE, verbose_name='Ответ')

    def __str__(self):
        template = '{0.option_choice.choice_name}'
        return template.format(self)


class Answer(models.Model):
    answer_set = models.ForeignKey(SurveyeeSurvey, on_delete=models.CASCADE, verbose_name='Набор ответов')
    surveyee = models.ForeignKey(Surveyee, on_delete=models.CASCADE, verbose_name='Анкетируемый', editable=False)
    question_option = models.ForeignKey(QuestionOption, on_delete=models.CASCADE, verbose_name='Ответ')
    answer_text = models.TextField(max_length=1000, blank=True, null=True, verbose_name='Текст ответа')

    def __str__(self):
        template = 'Ответ №{0.id}. {0.surveyee}, {0.answer_set.survey}'
        return template.format(self)

    class Meta:
        verbose_name = 'Ответ'
        verbose_name_plural = 'Ответы'
