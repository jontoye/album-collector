from django.db import models

"""
Rolling Stones
22bE4uQ6baNwSHPVcDxLCe
https://i.scdn.co/image/ab6761610000e5ebd3cb15a8570cce5a63af63d8
"""


class Artist(models.Model):
    id = models.CharField(primary_key=True, max_length=50)
    name = models.CharField(max_length=100)
    image_url = models.CharField(max_length=300, blank=True)
    spotify_followers = models.IntegerField(blank=True)
    # genres = models.ManyToManyField(Genre)
