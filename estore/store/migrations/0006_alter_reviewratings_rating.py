# Generated by Django 4.2.7 on 2024-03-06 10:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0005_rename_reviewrattings_reviewratings'),
    ]

    operations = [
        migrations.AlterField(
            model_name='reviewratings',
            name='rating',
            field=models.FloatField(blank=True),
        ),
    ]
