# Generated by Django 5.0.1 on 2024-02-22 14:21

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='account',
            name='date_joined',
            field=models.DateField(null=True, verbose_name=datetime.datetime(2024, 2, 22, 14, 21, 55, 735870, tzinfo=datetime.timezone.utc)),
        ),
    ]
