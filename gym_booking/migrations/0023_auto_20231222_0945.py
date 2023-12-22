# Generated by Django 3.2.1 on 2023-12-22 08:45

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('gym_booking', '0022_alter_gymmembership_plan'),
    ]

    operations = [
        migrations.RenameField(
            model_name='gymmembership',
            old_name='expiry_date',
            new_name='expiration_date',
        ),
        migrations.RemoveField(
            model_name='payment',
            name='plan',
        ),
        migrations.AlterField(
            model_name='gymmembership',
            name='created_at',
            field=models.DateTimeField(default=django.utils.timezone.now, null=True),
        ),
        migrations.AlterField(
            model_name='gymmembership',
            name='plan',
            field=models.CharField(default='', max_length=20),
        ),
        migrations.AlterField(
            model_name='payment',
            name='ref',
            field=models.CharField(max_length=5),
        ),
        migrations.DeleteModel(
            name='Subscription',
        ),
    ]
