from django.apps import AppConfig


class SurveyConfig(AppConfig):
    default_auto_field = 'hashid_field.BigHashidAutoField'
    name = 'survey'
    verbose_name = 'Анкеты'
