
import os
from pprint import pprint
import requests
import json
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.db.models import Q
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from .models import Album

# API configuration
API_SPOTIFY_HEADERS = {
    "X-RapidAPI-Host": os.environ.get('ALBUMCOL_API_HOST'),
    "X-RapidAPI-Key": os.environ.get('ALBUMCOL_API_KEY')
}
auth_manager = SpotifyClientCredentials()
spotify = spotipy.Spotify(auth_manager=auth_manager)


def home(request):
    new_releases = []
    results = spotify.new_releases(country='CA')
    dataset = results['albums']['items']

    for album in dataset:

        new_releases.append({
            'id': album['id'],
            'name': album['name'],
            'artist': album['artists'][0]['name'],
            'cover_art': album['images'][0]['url'] if album['images'] else '/static/images/favicon.png',
            'date': album['release_date'],
            'spotify_uri': album['uri']
        })

    context = {'albums': new_releases}

    return render(request, 'main_app/home.html', context)


def signup(request):
    error_message = ''
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('view_collection')
        else:
            error_message = 'Invalid sign up - try again'
    form = UserCreationForm()
    context = {'form': form, 'error_message': error_message}
    return render(request, 'registration/signup.html', context)


def search_by_artist(request):
    artists = []
    count = 0
    query = request.GET.get('q') if request.GET.get('q') is not None else ''

    if query:
        results = spotify.search(q=query, type='artist')
        count = results['artists']['total']
        dataset = results['artists']['items']

        for artist in dataset:

            artists.append({
                'id': artist['id'],
                'name': artist['name'],
                'avatar_img': artist['images'][0]['url'] if artist['images'] else '/static/images/favicon.png',
                'genres': artist['genres'],
                'followers': artist['followers']['total'],
                'href': artist['href']
            })

    context = {'artists': artists, 'count': count, 'query': query}
    return render(request, 'main_app/artists.html', context)


def search_by_album(request):
    count = 0
    albums = []
    query = request.GET.get('q') if request.GET.get('q') is not None else ''

    if query:
        results = spotify.search(q=query, type='album', limit=20)
        count = results['albums']['total']
        dataset = results['albums']['items']

        for album in dataset:

            albums.append({
                'id': album['id'],
                'name': album['name'],
                'artist': album['artists'][0]['name'],
                'cover_art': album['images'][0]['url'] if album['images'] else '/static/images/favicon.png',
                'date': album['release_date'],
                'spotify_uri': album['uri']
            })

    context = {'albums': albums, 'count': count, 'query': query}
    return render(request, 'main_app/albums.html', context)


def artist_detail(request, artist_id):
    albums = []

    artist_data = spotify.artist(artist_id)

    url = "https://spotify23.p.rapidapi.com/artist_overview/"
    querystring = {"id": artist_id}
    response = requests.request("GET", url, headers=API_SPOTIFY_HEADERS, params=querystring)
    artist_extra_data = json.loads(response.text)['data']['artist']

    artist = {
        'id': artist_data['id'],
        'name': artist_data['name'],
        'avatar_img': artist_data['images'][0]['url'] if artist_data['images'] else '/static/images/favicon.png',
        'followers': artist_data['followers']['total'],
        'href': artist_data['href'],

        # 'biography': '',
        'biography': artist_extra_data['profile']['biography']['text'] if artist_extra_data['profile']['biography']['text'] else '',
        'header_img': artist_extra_data['visuals']['headerImage']['sources'][0]['url'] if artist_extra_data['visuals']['headerImage'] else '',
    }

    album_data = spotify.artist_albums(artist_id=artist_id, album_type='album', limit=50)
    for album in album_data['items']:
        albums.append({
            'id': album['id'],
            'name': album['name'],
            'cover_art': album['images'][0]['url'] if album['images'] else '/static/images/favicon.png',
            'date': album['release_date'],
            'spotify_uri': album['uri']
        })

    # pprint(albums)
    context = {'artist': artist, 'albums': albums}
    return render(request, 'main_app/artist_detail.html', context)


def album_detail(request, album_id):
    is_owned_by_user = False
    album_data = spotify.album(album_id)

    album = {
        'id': album_data['id'],
        'artist': album_data['artists'][0]['name'],
        'name': album_data['name'],
        'cover_art': album_data['images'][0]['url'] if album_data['images'] else '/static/images/favicon.png',
        'date': album_data['release_date'],
        'spotify_uri': album_data['uri'],
        'tracks': album_data['tracks']['items']
    }

    try:
        a = Album.objects.get(id=album_id)
        if a.owners.get(id=request.user.id) == request.user:
            is_owned_by_user = True
    except Album.DoesNotExist:
        pass

    return render(request, 'main_app/album_detail.html', {'album': album, 'is_owned_by_user': is_owned_by_user})


def view_collection(request):
    albums = Album.objects.filter(owners=request.user.id)
    return render(request, 'main_app/mycollection.html', {'albums': albums})


def add_to_collection(request, album_id):
    print('adding album', album_id)
    album_data = spotify.album(album_id)

    album, created = Album.objects.get_or_create(
        id=album_data['id'],
        name=album_data['name'],
        artist=album_data['artists'][0]['name'],
        cover_art=album_data['images'][0]['url'] if album_data['images'] else '/static/images/favicon.png',
        date=album_data['release_date'],
        spotify_uri=album_data['uri'],
    )
    if created:
        album.owners.add(request.user.id)

    return redirect('view_collection')


def remove_from_collection(request, album_id):

    a = Album.objects.get(id=album_id)
    a.owners.remove(request.user.id)

    print('removed album from your collection')
    return redirect('view_collection')


def view_top_albums(request):
    pass
