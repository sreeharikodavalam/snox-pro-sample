# Generated by Django 5.0 on 2023-12-09 02:11

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='UserSelfie',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user_name', models.CharField(max_length=255)),
                ('mobile_number', models.CharField(max_length=15)),
                ('selfie_image', models.ImageField(upload_to='user_selfies/')),
            ],
        ),
    ]