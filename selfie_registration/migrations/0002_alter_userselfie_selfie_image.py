# Generated by Django 5.0 on 2023-12-09 02:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('selfie_registration', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userselfie',
            name='selfie_image',
            field=models.ImageField(upload_to='uploads/user_selfies/'),
        ),
    ]