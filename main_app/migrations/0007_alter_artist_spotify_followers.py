# Generated by Django 4.0.3 on 2022-03-30 21:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main_app', '0006_alter_album_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='artist',
            name='spotify_followers',
            field=models.IntegerField(blank=True, null=True),
        ),
    ]
