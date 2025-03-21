# Generated by Django 5.0.7 on 2024-08-25 13:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user_profile', '0002_alter_userprofile_profile_country'),
    ]

    operations = [
        migrations.AddField(
            model_name='userprofile',
            name='profile_date_of_birth',
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='userprofile',
            name='profile_title',
            field=models.CharField(blank=True, choices=[('None', 'Prefer not to use'), ('Mr', 'Mr.'), ('Mrs', 'Mrs.'), ('Ms', 'Ms.'), ('Miss', 'Miss'), ('Dr', 'Dr.'), ('Prof', 'Prof.'), ('Mx', 'Mx.'), ('Rev', 'Rev.'), ('Sir', 'Sir'), ('Dame', 'Dame')], max_length=5, null=True),
        ),
    ]
