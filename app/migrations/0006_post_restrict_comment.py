# Generated by Django 3.2 on 2021-04-07 21:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0005_comment'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='restrict_comment',
            field=models.BooleanField(default=False),
        ),
    ]
