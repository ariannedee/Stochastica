# Generated by Django 2.1.7 on 2019-03-01 00:17

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('presentation', '0002_auto_20190208_0105'),
    ]

    operations = [
        migrations.AlterField(
            model_name='pack',
            name='subscribers',
            field=models.ManyToManyField(blank=True, null=True, related_name='subscribed_to', to=settings.AUTH_USER_MODEL),
        ),
    ]
