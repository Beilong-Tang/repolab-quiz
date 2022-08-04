# Generated by Django 4.0.5 on 2022-07-26 06:37

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('simple_judge', '0025_merge_20220726_1437'),
    ]

    operations = [
        migrations.AddField(
            model_name='question',
            name='logx',
            field=models.TextField(default=''),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='question',
            name='due_date',
            field=models.DateTimeField(default=datetime.datetime(2022, 7, 14, 15, 59, tzinfo=utc), verbose_name='date due'),
        ),
        migrations.AlterField(
            model_name='question',
            name='pub_date',
            field=models.DateTimeField(default=datetime.datetime(2022, 7, 13, 15, 59, tzinfo=utc), verbose_name='date published'),
        ),
        migrations.AlterField(
            model_name='question',
            name='question_title',
            field=models.CharField(max_length=50),
        ),
    ]
