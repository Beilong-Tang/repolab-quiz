# Generated by Django 4.0.5 on 2022-12-14 09:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('simple_judge', '0043_remove_question_logx_json'),
    ]

    operations = [
        migrations.AddField(
            model_name='question',
            name='seed',
            field=models.IntegerField(default=0),
        ),
    ]
