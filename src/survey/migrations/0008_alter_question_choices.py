# Generated by Django 3.2.4 on 2021-06-26 19:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('survey', '0007_questiontype_desc'),
    ]

    operations = [
        migrations.AlterField(
            model_name='question',
            name='choices',
            field=models.TextField(blank=True, help_text='Оставить поле пустым, если выбран тип ответа в свободной форме', max_length=500, null=True, verbose_name='Варианты ответа'),
        ),
    ]
