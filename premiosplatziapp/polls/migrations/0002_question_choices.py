# Generated by Django 4.1 on 2022-08-19 14:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('polls', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='question',
            name='choices',
            field=models.IntegerField(default=0),
        ),
    ]
