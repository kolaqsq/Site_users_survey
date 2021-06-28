# Generated by Django 3.2.4 on 2021-06-24 20:25

import ckeditor_uploader.fields
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('survey', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='survey',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, null=True, verbose_name='Дата создания'),
        ),
        migrations.AddField(
            model_name='survey',
            name='created_by',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='Автор'),
        ),
        migrations.AddField(
            model_name='survey',
            name='desc',
            field=ckeditor_uploader.fields.RichTextUploadingField(blank=True, max_length=1000, null=True, verbose_name='Описание'),
        ),
        migrations.AddField(
            model_name='survey',
            name='is_open',
            field=models.BooleanField(blank=True, null=True, verbose_name='Открыто'),
        ),
        migrations.AddField(
            model_name='survey',
            name='updated_at',
            field=models.DateTimeField(auto_now=True, null=True, verbose_name='Дата последнего изменения'),
        ),
        migrations.AlterField(
            model_name='survey',
            name='title',
            field=models.CharField(max_length=200, verbose_name='Название'),
        ),
    ]