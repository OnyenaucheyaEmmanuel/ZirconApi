# Generated by Django 3.2.1 on 2023-12-21 12:44

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('gym_booking', '0012_alter_payment_plan'),
    ]

    operations = [
        migrations.AlterField(
            model_name='payment',
            name='plan',
            field=models.ForeignKey(blank=True, default='', null=True, on_delete=django.db.models.deletion.CASCADE, to='gym_booking.gymmembership'),
        ),
    ]
