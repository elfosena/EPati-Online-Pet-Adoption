# Generated by Django 4.0.5 on 2022-06-20 10:18

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('adopt', '0012_remove_pet_kind'),
    ]

    operations = [
        migrations.RenameField(
            model_name='pet',
            old_name='kindfk',
            new_name='kind',
        ),
    ]
