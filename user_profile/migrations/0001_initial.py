# Generated by Django 5.0.7 on 2024-08-24 22:38

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='UserProfile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('profile_phone_number', models.CharField(blank=True, max_length=20, null=True)),
                ('profile_street_address', models.CharField(blank=True, max_length=80, null=True)),
                ('profile_town_city', models.CharField(blank=True, max_length=40, null=True)),
                ('profile_county', models.CharField(blank=True, max_length=80, null=True)),
                ('profile_postcode', models.CharField(blank=True, max_length=20, null=True)),
                ('profile_country', models.CharField(blank=True, max_length=40, null=True)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]