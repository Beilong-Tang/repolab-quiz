# Generated by Django 4.0.5 on 2022-07-02 23:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('simple_judge', '0008_remove_question_question_content'),
    ]

    operations = [
        migrations.AddField(
            model_name='question',
            name='question_content',
            field=models.JSONField(default=1, verbose_name='quiz_content'),
            preserve_default=False,
        ),
    ]
