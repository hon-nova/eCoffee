# Generated by Django 5.0.6 on 2024-06-29 18:00

import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('eCoffee', '0012_orderitem'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='placed_order_at',
            field=models.DateTimeField(blank=True, default=django.utils.timezone.now, null=True),
        ),
    ]
