# Generated by Django 4.0.5 on 2022-08-02 11:14

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('simple_judge', '0033_alter_student_student_name_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='student',
            name='offline_time',
            field=models.DateTimeField(default=datetime.datetime(2022, 7, 25, 22, 30, tzinfo=utc)),
        ),
        migrations.AddField(
            model_name='student',
            name='online_time',
            field=models.DateTimeField(default=datetime.datetime(2022, 7, 25, 22, 0, tzinfo=utc)),
        ),
    ]
