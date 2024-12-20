# Generated by Django 5.0.7 on 2024-08-30 12:21

import django.db.models.deletion
import django_countries.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user_profile', '0003_userprofile_profile_date_of_birth_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userprofile',
            name='profile_street_address',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.CreateModel(
            name='ShippingAddress',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('full_name', models.CharField(max_length=50)),
                ('phone_number', models.CharField(max_length=20)),
                ('email', models.EmailField(max_length=254)),
                ('delivery_name', models.CharField(max_length=50)),
                ('shipping_street_address', models.CharField(max_length=255)),
                ('shipping_town_city', models.CharField(max_length=40)),
                ('shipping_county', models.CharField(max_length=80)),
                ('shipping_postcode', models.CharField(max_length=20)),
                ('shipping_country', django_countries.fields.CountryField(max_length=2)),
                ('user_profile', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='addresses', to='user_profile.userprofile')),
            ],
        ),
    ]
