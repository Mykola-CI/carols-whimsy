# Generated by Django 5.0.7 on 2024-08-24 22:47

import django_countries.fields
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('user_profile', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userprofile',
            name='profile_country',
            field=django_countries.fields.CountryField(blank=True, max_length=2, null=True),
        ),
    ]