# Generated by Django 5.0.7 on 2024-08-13 14:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('checkout', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='order',
            old_name='full_name',
            new_name='last_name',
        ),
        migrations.RemoveField(
            model_name='order',
            name='street_address1',
        ),
        migrations.RemoveField(
            model_name='order',
            name='street_address2',
        ),
        migrations.AddField(
            model_name='order',
            name='first_name',
            field=models.CharField(default='First Name', max_length=40),
        ),
        migrations.AddField(
            model_name='order',
            name='street_address',
            field=models.CharField(default='No address', max_length=254),
            preserve_default=False,
        ),
    ]