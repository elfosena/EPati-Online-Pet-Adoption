# Generated by Django 4.0.5 on 2022-06-11 22:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('adopt', '0007_pet_published_by_alter_pet_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='pet',
            name='age',
            field=models.CharField(choices=[('YOUNG', 'Young'), ('ADULT', 'Adult'), ('SENIOR', 'Senior')], max_length=50),
        ),
    ]
