# Generated by Django 2.1.7 on 2019-06-05 21:44

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('presentation', '0004_game'),
    ]

    operations = [
        migrations.AddField(
            model_name='game',
            name='game_duration',
            field=models.TimeField(default=datetime.time(0, 2)),
        ),
    ]
