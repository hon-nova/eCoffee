# Generated by Django 5.0.6 on 2024-06-24 20:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('eCoffee', '0007_profile'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='payment_intent_id',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
    ]