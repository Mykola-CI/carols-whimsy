# Generated by Django 5.0.7 on 2024-09-07 19:08

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('checkout', '0010_order_saving'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='order',
            name='shipping_address',
        ),
    ]
