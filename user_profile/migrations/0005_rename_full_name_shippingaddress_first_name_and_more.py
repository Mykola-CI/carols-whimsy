# Generated by Django 5.0.7 on 2024-08-30 13:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user_profile', '0004_alter_userprofile_profile_street_address_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='shippingaddress',
            old_name='full_name',
            new_name='first_name',
        ),
        migrations.AddField(
            model_name='shippingaddress',
            name='last_name',
            field=models.CharField(default='', max_length=50),
            preserve_default=False,
        ),
    ]
