from django.contrib.auth.models import User
from django.db import models


class Survey(models.Model):
    creator = models.ForeignKey(User, on_delete=models.CASCADE, default=2, verbose_name='Создатель')
    survey_title = models.CharField('Название анкеты', max_length=200)
    survey_desc = models.TextField('Описание анкеты', max_length=500, blank=True, null=True)
    creation_date = models.DateTimeField('Дата публикации')
    is_open = models.BooleanField('Открыто для заполнения')

    def __str__(self):
        return self.survey_title

    class Meta:
        verbose_name = 'Анкета'
        verbose_name_plural = 'Анкеты'


class Section(models.Model):
    survey = models.ForeignKey(Survey, on_delete=models.CASCADE, verbose_name='Анкета')
    section_title = models.CharField('Название секции', max_length=200)
    section_desc = models.TextField('Описание секции', max_length=500, blank=True, null=True)

    def __str__(self):
        return self.section_title

    class Meta:
        verbose_name = 'Секция анкеты'
        verbose_name_plural = 'Секции анкеты'


class QuestionType(models.Model):
    type_name = models.CharField('Тип вопроса', max_length=50)

    def __str__(self):
        return self.type_name

    class Meta:
        verbose_name = 'Тип вопросов'
        verbose_name_plural = 'Типы вопросов'


class OptionGroup(models.Model):
    group_name = models.CharField('Тип ответа', max_length=200)

    def __str__(self):
        return self.group_name

    class Meta:
        verbose_name = 'Тип ответов'
        verbose_name_plural = 'Типы ответов'


class OptionChoice(models.Model):
    group = models.ForeignKey(OptionGroup, on_delete=models.CASCADE, verbose_name='Тип ответов')
    choice_name = models.CharField('Вариант ответа', max_length=250, blank=True, null=True)

    def __str__(self):
        return self.group_id, self.choice_name

    class Meta:
        verbose_name = 'Вариант ответов'
        verbose_name_plural = 'Варианты ответов'


class Question(models.Model):
    survey = models.ForeignKey(Survey, on_delete=models.CASCADE, verbose_name='Анкета')
    section = models.ForeignKey(Section, on_delete=models.CASCADE, default=1, verbose_name='Секция')
    question_type = models.ForeignKey(QuestionType, on_delete=models.DO_NOTHING, verbose_name='Тип вопроса')
    option_group = models.ForeignKey(OptionGroup, on_delete=models.DO_NOTHING, default=1, verbose_name='Тип ответа')
    question_text = models.TextField('Вопрос', max_length=500)

    def __str__(self):
        return self.question_text

    class Meta:
        verbose_name = 'Вопрос'
        verbose_name_plural = 'Вопросы'


class QuestionOption(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    option_choice = models.ForeignKey(OptionChoice, on_delete=models.CASCADE)
