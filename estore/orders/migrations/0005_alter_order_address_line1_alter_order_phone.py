# Generated by Django 4.2.7 on 2024-02-26 22:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0004_alter_order_address_line1_alter_order_payment_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='address_line1',
            field=models.CharField(max_length=50),
        ),
        migrations.AlterField(
            model_name='order',
            name='phone',
            field=models.CharField(max_length=50),
        ),
    ]