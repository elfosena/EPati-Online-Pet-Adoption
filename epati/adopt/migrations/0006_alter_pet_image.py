# Generated by Django 4.0.5 on 2022-06-08 14:29

import django.core.files.storage
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('adopt', '0005_alter_pet_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='pet',
            name='image',
            field=models.ImageField(null=True, storage=django.core.files.storage.FileSystemStorage(location='/media'), upload_to='pics'),
        ),
    ]
