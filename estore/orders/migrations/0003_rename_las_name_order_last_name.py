# Generated by Django 4.2.7 on 2024-02-26 15:38

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0002_rename_phone_number_order_phone'),
    ]

    operations = [
        migrations.RenameField(
            model_name='order',
            old_name='las_name',
            new_name='last_name',
        ),
    ]
