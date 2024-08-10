# Generated by Django 5.0.6 on 2024-08-07 22:54

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('currency', '0001_initial'),
        ('plans', '0004_alter_operation_currency'),
        ('users', '0002_alter_user_currency'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='currency',
            field=models.ForeignKey(blank=True, default=1, null=True, on_delete=django.db.models.deletion.CASCADE, to='currency.currency'),
        ),
        migrations.DeleteModel(
            name='Currency',
        ),
    ]