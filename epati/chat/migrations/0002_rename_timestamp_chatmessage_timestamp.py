# Generated by Django 4.0.5 on 2022-07-04 09:31

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('chat', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='chatmessage',
            old_name='Timestamp',
            new_name='timestamp',
        ),
    ]