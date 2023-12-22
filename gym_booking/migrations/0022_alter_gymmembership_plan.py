# Generated by Django 3.2.1 on 2023-12-22 08:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('gym_booking', '0021_auto_20231222_0936'),
    ]

    operations = [
        migrations.AlterField(
            model_name='gymmembership',
            name='plan',
            field=models.CharField(choices=[('No Plan', 'No Plan'), ('bronze', 'Bronze'), ('silver', 'Silver'), ('gold', 'Gold')], default='No Plan', max_length=10),
        ),
    ]
