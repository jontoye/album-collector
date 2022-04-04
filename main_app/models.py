from django.db import models
from django.contrib.auth.models import User


# class Genre(models.Model):
#     name = models.CharField(max_length=50)

#     def __str__(self):
#         return self.name


class Album(models.Model):
    id = models.CharField(primary_key=True, max_length=50)
    name = models.CharField(max_length=100)
    artist = models.CharField(max_length=200, blank=True)
    cover_art = models.CharField(max_length=200, blank=True)
    date = models.CharField(max_length=20, blank=True)
    spotify_uri = models.CharField(max_length=200, blank=True)
    owners = models.ManyToManyField(User)
    # label = models.CharField(max_length=100, blank=True)
    # tracks = models.ManyToManyField(Track)
    # reviews =

    def __str__(self):
        return self.name


# class Artist(models.Model):
#     id = models.CharField(primary_key=True, max_length=50)
#     name = models.CharField(max_length=100)
#     biography = models.CharField(max_length=100000, blank=True, default='')
#     header_img = models.CharField(max_length=300, blank=True)
#     avatar_img = models.CharField(max_length=300, blank=True)
#     spotify_uri = models.CharField(max_length=200, blank=True)
#     spotify_followers = models.IntegerField(blank=True, default=0)
#     world_rank = models.IntegerField(default=9999999)
#     genres = models.ManyToManyField(Genre)
#     albums = models.ManyToManyField(Album)

#     class Meta:
#         ordering = ['-spotify_followers']

#     def __str__(self):
#         return self.name
