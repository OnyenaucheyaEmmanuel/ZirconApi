# Generated by Django 3.2.1 on 2023-12-22 08:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('gym_booking', '0016_remove_payment_plan'),
    ]

    operations = [
        migrations.AddField(
            model_name='payment',
            name='plan',
            field=models.CharField(choices=[('No Plan', 'No Plan'), ('bronze', 'Bronze'), ('silver', 'Silver'), ('gold', 'Gold')], default='No Plan', max_length=10),
        ),
    ]
