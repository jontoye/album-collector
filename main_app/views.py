
import os
from django.http import HttpResponse
import requests
import json
import time
from urllib.parse import quote
from django.shortcuts import render
from datetime import date
from .models import Artist, Album, Genre
from django.db.models import Q
import pprint

API_SPOTIFY_HEADERS = {
    "X-RapidAPI-Host": os.environ.get('ALBUMCOL_API_HOST'),
    "X-RapidAPI-Key": os.environ.get('ALBUMCOL_API_KEY')
}


def home(request):
    return render(request, 'main_app/home.html')


def search_by_artist(request):
    context = {}
    if request.method == 'POST':
        query = request.POST.get('q')
        artists = Artist.objects.filter(name__icontains=query)
        print(f"Found {artists.count()} matches in db")

        # need to call API
        if artists.count() == 0:
            artists = fetch_artists(query)

        context['artists'] = artists
        context['query'] = query
    return render(request, 'main_app/artists.html', context)


def search_by_album(request):
    if request.method == 'POST':
        query = request.POST.get('q')

    context = {'search_type': 'album'}
    return render(request, 'main_app/albums.html', context)


def artist_detail(request, artist_id):
    try:
        artist = Artist.objects.get(id=artist_id)
    except Artist.DoesNotExist:
        artist = fetch_artist_details(artist_id)

    if artist.biography == '':
        artist = update_artist_details(artist)
    context = {'artist': artist, 'albums': artist.albums.all()}
    return render(request, 'main_app/artist_detail.html', context)


def album_detail(request, album_id):
    pass


def view_collection(request):
    pass


def view_top_albums(request):
    pass


def fetch_artists(query):
    print('-----FETCHING ARTISTS FROM SPOTIFY---------')
    url = "https://spotify23.p.rapidapi.com/search/"
    querystring = {"q": query, "type": "artists", "limit": 10}
    response = requests.request("GET", url, headers=API_SPOTIFY_HEADERS, params=querystring)
    print(response.status_code)
    artists = json.loads(response.text)['artists']['items']

    for artist in artists:
        data = artist['data']
        name = data['profile']['name'].replace('-', ' ')
        uri = data['uri']
        id = uri.split(':')[-1]
        avatar_img = data['visuals']['avatarImage']['sources'][0]['url'] if data['visuals']['avatarImage'] else ''

        # save to db
        Artist.objects.create(
            id=id,
            name=name,
            spotify_uri=uri,
            avatar_img=avatar_img
        )
        print(f"added {data['profile']['name']} to db")

    return Artist.objects.filter(name__icontains=query)


def fetch_artist_details(artist_id):
    """Gets artist details and creates new db entry"""
    print('-----CREATING NEW ARTIST AND ALBUMS---------')
    url = "https://spotify23.p.rapidapi.com/artist_overview/"
    querystring = {"id": artist_id}
    response = requests.request("GET", url, headers=API_SPOTIFY_HEADERS, params=querystring)
    data = json.loads(response.text)['data']['artist']

    artist = Artist.objects.create(
        id=data[id],
        name=data['profile']['name'],
        biography=data['profile']['biography']['text'] if data['profile']['biography']['text'] else '',
        header_img=data['visuals']['headerImage']['sources'][0]['url'] if data['visuals']['headerImage'] else '',
        avatar_img=data['visuals']['avatarImage']['sources'][0]['url'] if data['visuals']['avatarImage'] else '',
        spotify_uri=data['uri'],
        spotify_followers=data['stats']['followers'],
        world_rank=data['stats']['worldRank']
    )
    print(f"Added artist {artist.name} to db")

    # create and add albums
    for album in data['discography']['albums']['items']:
        field = album['releases']['items'][0]
        new_album = Album.objects.create(
            id=field['id'],
            name=field['name'],
            date=field['date']['year'],
            cover_art=field['coverArt']['sources'][0]['url'],
            label=field['label'],
            spotify_uri=field['uri']
        )
        artist.albums.add(new_album)
        print(f"Added album {album.name} to db")

    return artist


def update_artist_details(artist):
    """Gets artist details and updates an existing artist record in db"""
    print('-----UPDATING ARTIST AND ALBUMS---------')
    url = "https://spotify23.p.rapidapi.com/artist_overview/"
    querystring = {"id": artist.id}
    response = requests.request("GET", url, headers=API_SPOTIFY_HEADERS, params=querystring)
    data = json.loads(response.text)['data']['artist']

    artist.biography = data['profile']['biography']['text'] if data['profile']['biography']['text'] else ''
    artist.header_img = data['visuals']['headerImage']['sources'][0]['url'] if data['visuals']['headerImage'] else ''
    artist.spotify_followers = data['stats']['followers']
    artist.world_rank = data['stats']['worldRank']
    artist.save()

    # create and add albums
    for album in data['discography']['albums']['items']:
        field = album['releases']['items'][0]
        new_album = Album.objects.create(
            id=field['id'],
            name=field['name'],
            date=field['date']['year'],
            cover_art=field['coverArt']['sources'][0]['url'],
            label=field['label'],
            spotify_uri=field['uri']
        )
        artist.albums.add(new_album)
        print(f"Added album {new_album.name} to db")

    return artist


def fetch_artist_genres(artist_id):
    url = "https://spotify23.p.rapidapi.com/artists/"
    querystring = {"ids": artist_id}
    response = requests.request("GET", url, headers=API_SPOTIFY_HEADERS, params=querystring)
    data = json.loads(response.text)
    data = data['artists'][0]
    genres = data['genres']

    return genres


def add_genres(artist, genres):
    for genre in genres:
        try:
            g = Genre.objects.get(name=genre)
        except Genre.DoesNotExist:
            g = Genre.objects.create(name=genre)

        artist.genres.add(g)
