# Generated by Django 4.0.5 on 2022-07-06 11:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('chat', '0002_rename_timestamp_chatmessage_timestamp'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='thread',
            unique_together=set(),
        ),
        migrations.AlterField(
            model_name='thread',
            name='timestamp',
            field=models.DateTimeField(auto_now_add=True),
        ),
    ]
