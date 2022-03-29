
import os
import requests
import json
from urllib.parse import quote
from django.shortcuts import render
from datetime import date
from .models import Artist, Album


def fetch_artist(artist_name):
    url = "https://spotify23.p.rapidapi.com/search/"

    querystring = {"q": artist_name, "type": "artists",
                   "offset": "0", "limit": "5", "numberOfTopResults": "5"}

    headers = {
        "X-RapidAPI-Host": os.environ.get('ALBUMCOL_API_HOST'),
        "X-RapidAPI-Key": os.environ.get('ALBUMCOL_API_KEY')
    }

    response = requests.request(
        "GET", url, headers=headers, params=querystring)

    data = json.loads(response.text)
    artist = data['artists']['items'][0]

    # save to db
    new_artist = Artist(
        id=artist['data']['uri'].split(':')[-1],
        name=artist['data']['profile']['name'],
        image_url=artist['data']['visuals']['avatarImage']['sources'][0]['url'],
        spotify_followers=0
    )
    new_artist.save()

    return artist


def fetch_albums_from_artist(artist_id):
    url = "https://spotify23.p.rapidapi.com/artist_albums/"

    querystring = {"id": artist_id, "offset": "0", "limit": "100"}

    headers = {
        "X-RapidAPI-Host": os.environ.get('ALBUMCOL_API_HOST'),
        "X-RapidAPI-Key": os.environ.get('ALBUMCOL_API_KEY')
    }

    response = requests.request(
        "GET", url, headers=headers, params=querystring)
    data = json.loads(response.text)
    albums = data['data']['artist']['discography']['albums']['items']

    # save to db
    for album in albums:
        field = album['releases']['items'][0]
        new_album = Album(
            id=field['id'],
            name=field['name'],
            artist=Artist.objects.get(pk=artist_id),
            date=date.fromisoformat(field['date']['isoString'][:10]),
            cover_art=field['coverArt']['sources'][0]['url']
        )
        new_album.save()

    return Album.objects.filter(artist__id=artist_id)


def home(request):
    context = {}
    artist_name = request.GET.get(
        'q') if request.GET.get('q') is not None else ''

    if artist_name is not '':
        # First, check database
        albums = Album.objects.filter(artist__name__icontains=artist_name)

        # If not in db, call api
        if len(albums) == 0:
            artist = fetch_artist(artist_name)
            artist_id = artist['data']['uri'].split(
                ':')[-1]  # extract artist id
            albums = fetch_albums_from_artist(artist_id)

        context = {'albums': albums, 'album_count': len(albums),
                   'artist_name': artist_name}
    return render(request, 'main_app/home.html', context)
