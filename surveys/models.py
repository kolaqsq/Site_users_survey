from django.contrib.auth.models import User
from django.db import models


class Survey(models.Model):
    creator = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Создатель', default=1, editable=False)
    survey_title = models.CharField('Название анкеты', max_length=200)
    survey_desc = models.TextField('Описание анкеты', max_length=500, blank=True, null=True)
    creation_date = models.DateTimeField('Дата публикации')
    is_open = models.BooleanField('Открыто для заполнения')

    def __str__(self):
        template = '{0.creator}, {0.survey_title}'
        return template.format(self)

    class Meta:
        verbose_name = 'Анкета'
        verbose_name_plural = 'Анкеты'


class Section(models.Model):
    creator = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Создатель', editable=False)
    survey = models.ForeignKey(Survey, on_delete=models.CASCADE, verbose_name='Анкета')
    section_title = models.CharField('Название секции', max_length=200)
    section_desc = models.TextField('Описание секции', max_length=500, blank=True, null=True)

    def __str__(self):
        template = '{0.creator}, {0.survey.survey_title}, {0.section_title}'
        return template.format(self)

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
    creator = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Создатель', editable=False)
    group_name = models.CharField('Тип ответа', max_length=200)

    def __str__(self):
        template = '{0.creator}, {0.group_name}'
        return template.format(self)

    class Meta:
        verbose_name = 'Тип ответов'
        verbose_name_plural = 'Типы ответов'


class OptionChoice(models.Model):
    group = models.ForeignKey(OptionGroup, on_delete=models.CASCADE, verbose_name='Тип ответов')
    choice_name = models.CharField('Вариант ответа', max_length=250, blank=True, null=True)

    def __str__(self):
        template = '{0.group.group_name}, {0.choice_name}'
        return template.format(self)

    class Meta:
        verbose_name = 'Вариант ответов'
        verbose_name_plural = 'Варианты ответов'


class Question(models.Model):
    section = models.ForeignKey(Section, on_delete=models.CASCADE, verbose_name='Секция')
    question_type = models.ForeignKey(QuestionType, on_delete=models.DO_NOTHING, verbose_name='Тип вопроса')
    option_group = models.ForeignKey(OptionGroup, on_delete=models.DO_NOTHING, default=1, verbose_name='Тип ответа')
    question_text = models.TextField('Вопрос', max_length=500)

    def __str__(self):
        template = 'Вопрос №{0.id}. {0.section.section_title}, {0.section.survey}'
        return template.format(self)

    class Meta:
        verbose_name = 'Вопрос'
        verbose_name_plural = 'Вопросы'


