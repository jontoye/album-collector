# Generated by Django 4.0.3 on 2022-03-31 05:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main_app', '0012_alter_artist_biography_and_more'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='artist',
            options={'ordering': ['-spotify_followers']},
        ),
        migrations.AlterField(
            model_name='artist',
            name='biography',
            field=models.CharField(blank=True, default='', max_length=100000),
        ),
    ]
