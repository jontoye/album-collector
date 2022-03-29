from multiprocessing import context
import os
from django.shortcuts import render
import requests
import json
from urllib.parse import quote


def get_artist(artist_name):
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
    return data


def get_albums_from_artist(artist_id):
    url = "https://spotify23.p.rapidapi.com/artist_albums/"

    querystring = {"id": artist_id, "offset": "0", "limit": "100"}

    headers = {
        "X-RapidAPI-Host": os.environ.get('ALBUMCOL_API_HOST'),
        "X-RapidAPI-Key": os.environ.get('ALBUMCOL_API_KEY')
    }

    response = requests.request(
        "GET", url, headers=headers, params=querystring)
    data = json.loads(response.text)
    return data


def home(request):
    context = {}
    artist_name = request.GET.get(
        'q') if request.GET.get('q') is not None else ''

    if artist_name is not '':
        artist_data = get_artist(artist_name)

        artist = artist_data['artists']['items'][0]    # use first match found
        artist_id = artist['data']['uri'].split(':')[-1]  # extract artist id

        album_data = get_albums_from_artist(artist_id)
        # print(album_data)
        album_count = album_data['data']['artist']['discography']['albums']["totalCount"]
        albums = album_data['data']['artist']['discography']['albums']['items']

        context = {'albums': albums, 'album_count': album_count,
                   'artist_name': artist_name}
    return render(request, 'main_app/home.html', context)
