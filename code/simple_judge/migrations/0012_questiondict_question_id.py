# Generated by Django 4.0.5 on 2022-07-04 08:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('simple_judge', '0011_questiondict_question_type'),
    ]

    operations = [
        migrations.AddField(
            model_name='questiondict',
            name='question_id',
            field=models.IntegerField(default=0),
        ),
    ]
