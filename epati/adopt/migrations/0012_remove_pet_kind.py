# Generated by Django 4.0.5 on 2022-06-20 10:12

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('adopt', '0011_pet_kindfk_alter_pet_kind'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='pet',
            name='kind',
        ),
    ]
