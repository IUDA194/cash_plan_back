# Generated by Django 5.0.6 on 2024-08-07 22:54

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Currency',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=228)),
                ('full_name', models.CharField(max_length=456)),
            ],
        ),
    ]
