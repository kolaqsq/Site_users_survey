from django.contrib.auth.models import User
from django.db import models


class Survey(models.Model):
    creator = models.ForeignKey(User, on_delete=models.CASCADE)
    survey_title = models.CharField('Название анкеты', max_length=200)
    creation_date = models.DateTimeField('Дата публикации')
    is_open = models.BooleanField('Открыто для заполнения')


class QuestionType(models.Model):
    type_name = models.CharField('Тип вопроса', max_length=50)


class Question(models.Model):
    survey = models.ForeignKey(Survey, on_delete=models.CASCADE)
    question_type = models.ForeignKey(QuestionType, on_delete=models.DO_NOTHING)
    question_text = models.TextField('Вопрос', max_length=500)
