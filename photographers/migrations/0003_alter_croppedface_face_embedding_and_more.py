# Generated by Django 5.0 on 2023-12-11 07:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('photographers', '0002_alter_croppedface_album_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='croppedface',
            name='face_embedding',
            field=models.JSONField(null=True),
        ),
        migrations.AlterField(
            model_name='croppedface',
            name='face_locations',
            field=models.JSONField(null=True),
        ),
    ]