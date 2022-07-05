# Generated by Django 4.0.5 on 2022-07-05 12:13

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('simple_judge', '0018_question_due_date_alter_question_pub_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='question',
            name='due_date',
            field=models.DateTimeField(default=datetime.datetime(2022, 7, 5, 12, 13, 30, 190873, tzinfo=utc), verbose_name='date due'),
        ),
        migrations.AlterField(
            model_name='question',
            name='pub_date',
            field=models.DateTimeField(default=datetime.datetime(2022, 7, 5, 12, 13, 30, 190852, tzinfo=utc), verbose_name='date published'),
        ),
    ]
