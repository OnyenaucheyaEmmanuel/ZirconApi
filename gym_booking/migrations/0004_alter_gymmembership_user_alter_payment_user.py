# Generated by Django 4.2.7 on 2023-12-07 09:16

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('gym_booking', '0003_customuser'),
    ]

    operations = [
        migrations.AlterField(
            model_name='gymmembership',
            name='user',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='gym_booking.customuser'),
        ),
        migrations.AlterField(
            model_name='payment',
            name='user',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='gym_booking.customuser'),
        ),
    ]