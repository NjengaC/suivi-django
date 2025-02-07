# Generated by Django 4.2.16 on 2024-11-17 15:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('entry', '0009_alter_parcel_tracking_number'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='is_active',
            field=models.BooleanField(default=True),
        ),
        migrations.AlterField(
            model_name='parcel',
            name='tracking_number',
            field=models.CharField(default='FI1SLL1M1Q', max_length=100, unique=True),
        ),
    ]
