# Generated by Django 4.0.2 on 2022-02-08 02:20

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('api_basic', '0003_rename_date_task_date_added'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='task',
            name='date_added',
        ),
        migrations.AddField(
            model_name='task',
            name='date',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
    ]