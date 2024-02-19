# Generated by Django 5.0.1 on 2024-02-07 12:33

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Variation',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('variation_cartegory', models.CharField(choices=[('color', 'color'), ('size', 'size')], max_length=100)),
                ('variation_value', models.CharField(max_length=200)),
                ('is_active', models.BooleanField(default=True)),
                ('created_at', models.DateField(auto_now=True)),
                ('Product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='store.product')),
            ],
        ),
    ]
