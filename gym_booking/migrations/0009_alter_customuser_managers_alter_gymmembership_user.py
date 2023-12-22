# Generated by Django 4.2.7 on 2023-12-12 07:56

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('gym_booking', '0008_alter_customuser_groups_and_more'),
    ]

    operations = [
        migrations.AlterModelManagers(
            name='customuser',
            managers=[
            ],
        ),
        migrations.AlterField(
            model_name='gymmembership',
            name='user',
            field=models.OneToOneField(db_column='user_id', on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]