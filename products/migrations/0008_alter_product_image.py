# Generated by Django 5.0.7 on 2024-08-29 14:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0007_brand_friendly_name'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to=''),
        ),
    ]
