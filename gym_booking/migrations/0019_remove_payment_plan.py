# Generated by Django 3.2.1 on 2023-12-22 08:34

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('gym_booking', '0018_alter_payment_plan'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='payment',
            name='plan',
        ),
    ]