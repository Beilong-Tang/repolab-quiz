# Generated by Django 4.0.5 on 2022-07-26 06:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('simple_judge', '0027_alter_question_submission_times'),
    ]

    operations = [
        migrations.AddField(
            model_name='question',
            name='question_id',
            field=models.IntegerField(default=0),
        ),
    ]
