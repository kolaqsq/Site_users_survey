# Generated by Django 3.1.5 on 2021-01-15 12:45

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('surveys', '0006_auto_20210115_1306'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='question',
            name='survey',
        ),
    ]
