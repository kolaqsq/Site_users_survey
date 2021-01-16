from django.db import models

from surveys.models import Survey, Question, OptionChoice


class Surveyee(models.Model):
    name = models.CharField('Имя', max_length=100)
    surname = models.CharField('Фамилия', max_length=100)
    email = models.CharField('E-mail', max_length=100)

    def __str__(self):
        return self.name, self.surname

    class Meta:
        verbose_name = 'Анкетируемый'
        verbose_name_plural = 'Анкетируемые'


class SurveyeeSurvey(models.Model):
    survey = models.ForeignKey(Survey, on_delete=models.CASCADE)
    surveyee = models.ForeignKey(Surveyee, on_delete=models.CASCADE, verbose_name='Анкетируемый')


class QuestionOption(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    option_choice = models.ForeignKey(OptionChoice, on_delete=models.CASCADE)


class Answer(models.Model):
    surveyee = models.ForeignKey(Surveyee, on_delete=models.CASCADE)
    question_option = models.ForeignKey(QuestionOption, on_delete=models.CASCADE)
    answer_text = models.TextField(max_length=1000)
