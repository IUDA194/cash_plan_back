# Generated by Django 5.0.6 on 2024-07-07 23:25

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('plans', '0001_initial'),
        ('users', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddField(
            model_name='operation',
            name='currency',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='users.currency'),
        ),
        migrations.AddField(
            model_name='operation',
            name='owner',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]
