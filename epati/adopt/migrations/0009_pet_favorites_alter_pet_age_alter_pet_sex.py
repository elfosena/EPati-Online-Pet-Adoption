# Generated by Django 4.0.5 on 2022-06-14 13:29

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('adopt', '0008_alter_pet_age'),
    ]

    operations = [
        migrations.AddField(
            model_name='pet',
            name='favorites',
            field=models.ManyToManyField(blank=True, related_name='favorite', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='pet',
            name='age',
            field=models.CharField(choices=[('Young', 'Young'), ('Adult', 'Adult'), ('Senior', 'Senior')], max_length=50),
        ),
        migrations.AlterField(
            model_name='pet',
            name='sex',
            field=models.CharField(choices=[('Male', 'male'), ('Female', 'female')], max_length=50),
        ),
    ]