# Generated by Django 4.0.5 on 2022-08-04 01:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('forum', '0003_post_level'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='title',
            field=models.CharField(default='', max_length=100),
            preserve_default=False,
        ),
    ]
