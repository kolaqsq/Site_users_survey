from django.contrib.auth.models import User
from django.db import models
# from ckeditor_uploader.fields import RichTextUploadingField


class Survey(models.Model):
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Автор')
    title = models.CharField('Название', max_length=200)
    # desc = RichTextUploadingField('Описание', max_length=1000, blank=True, null=True)
    desc = models.TextField('Описание', max_length=1000, blank=True, null=True)
    is_open = models.BooleanField('Открыто')
    created_at = models.DateTimeField('Дата создания', auto_now_add=True)
    updated_at = models.DateTimeField('Дата последнего изменения', auto_now=True)

    def __str__(self):
        template = '{0.title}'
        return template.format(self)

    class Meta:
        verbose_name = 'Анкета'
        verbose_name_plural = 'Анкеты'


class Section(models.Model):
    survey = models.ForeignKey(Survey, on_delete=models.CASCADE, verbose_name='Анкета')
    title = models.CharField('Название', max_length=200)
    # desc = RichTextUploadingField('Описание', max_length=1000, blank=True, null=True)
    desc = models.TextField('Описание', max_length=1000, blank=True, null=True)
    created_at = models.DateTimeField('Дата создания', auto_now_add=True)
    updated_at = models.DateTimeField('Дата последнего изменения', auto_now=True)

    def __str__(self):
        template = '{0.title}'
        return template.format(self)

    class Meta:
        verbose_name = 'Секция анкеты'
        verbose_name_plural = 'Секции анкеты'


class QuestionType(models.Model):
    name = models.CharField('Тип вопроса', max_length=50)
    # desc = RichTextUploadingField('Описание', max_length=1000, blank=True, null=True)
    desc = models.TextField('Описание', max_length=1000, blank=True, null=True)

    def __str__(self):
        template = '{0.name}'
        return template.format(self)

    class Meta:
        verbose_name = 'Тип вопроса'
        verbose_name_plural = 'Типы вопросов'


class Question(models.Model):
    section = models.ForeignKey(Section, on_delete=models.CASCADE, verbose_name='Секция')
    title = models.CharField('Название', max_length=200)
    type = models.ForeignKey(QuestionType, on_delete=models.DO_NOTHING, verbose_name='Тип вопроса')
    # question = RichTextUploadingField('Вопрос', max_length=1000)
    question = models.TextField('Вопрос', max_length=1000)
    choices = models.TextField('Варианты ответа', max_length=500, blank=True, null=True,
                               help_text='Каждый вариант ответа вводить с новой строки.'
                                         'Оставить поле пустым, если выбран тип ответа в свободной форме')
    created_at = models.DateTimeField('Дата создания', auto_now_add=True)
    updated_at = models.DateTimeField('Дата последнего изменения', auto_now=True)

    def __str__(self):
        template = '{0.title}'
        return template.format(self)

    def choices_as_list(self):
        return self.choices.split('\n')

    class Meta:
        verbose_name = 'Вопрос'
        verbose_name_plural = 'Вопросы'


class AnswerSet(models.Model):
    survey = models.ForeignKey(Survey, on_delete=models.CASCADE, verbose_name='Анкета')
    created_at = models.DateTimeField('Дата создания', auto_now_add=True)

    def __str__(self):
        template = 'Набор ответов {0.id}'
        return template.format(self)

    class Meta:
        verbose_name = 'Набор ответов'
        verbose_name_plural = 'Наборы ответов'


class AnswerSubset(models.Model):
    set = models.ForeignKey(AnswerSet, on_delete=models.CASCADE, verbose_name='Нпбор ответов')
    section = models.ForeignKey(Section, on_delete=models.CASCADE, verbose_name='Секция')
    created_at = models.DateTimeField('Дата создания', auto_now_add=True)

    def __str__(self):
        template = 'Набор ответов на секцию {0.section.title}'
        return template.format(self)

    class Meta:
        verbose_name = 'Набор ответов на секцию'
        verbose_name_plural = 'Наборы ответов на секцию'


class Answer(models.Model):
    subset = models.ForeignKey(AnswerSubset, on_delete=models.CASCADE, verbose_name='Набор ответов на секцию')
    question = models.ForeignKey(Question, on_delete=models.CASCADE, verbose_name='Вопрос')
    answer = models.TextField('Ответ', max_length=500, blank=True, null=True)
    created_at = models.DateTimeField('Дата создания', auto_now_add=True)

    def __str__(self):
        template = 'Ответ на вопрос {0.question.title}'
        return template.format(self)

    class Meta:
        verbose_name = 'Ответ'
        verbose_name_plural = 'Ответы'
