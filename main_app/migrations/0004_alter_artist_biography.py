# Generated by Django 4.0.3 on 2022-03-30 03:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main_app', '0003_rename_image_url_artist_avatar_img_album_label_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='artist',
            name='biography',
            field=models.CharField(blank=True, max_length=6000),
        ),
    ]
