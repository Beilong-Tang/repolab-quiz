# Generated by Django 4.0.5 on 2022-07-26 06:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('simple_judge', '0026_question_logx_alter_question_due_date_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='question',
            name='submission_times',
            field=models.IntegerField(default=5),
        ),
    ]
