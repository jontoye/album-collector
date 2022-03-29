from django.db import models

"""
Rolling Stones
22bE4uQ6baNwSHPVcDxLCe
https://i.scdn.co/image/ab6761610000e5ebd3cb15a8570cce5a63af63d8
"""


class Genre(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name


class Artist(models.Model):
    id = models.CharField(primary_key=True, max_length=50)
    name = models.CharField(max_length=100)
    image_url = models.CharField(max_length=300, blank=True)
    spotify_uri = models.CharField(max_length=200, blank=True)
    spotify_followers = models.IntegerField(blank=True)
    genres = models.ManyToManyField(Genre)

    def __str__(self):
        return self.name


class Album(models.Model):
    id = models.CharField(primary_key=True, max_length=50)
    name = models.CharField(max_length=100)
    artist = models.ForeignKey(Artist, on_delete=models.CASCADE)
    date = models.DateField()
    cover_art = models.CharField(max_length=200)
    # tracks = models.ManyToManyField(Track)
    # owners =
    # reviews =

    def __str__(self):
        return self.name
