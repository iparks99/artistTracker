import json
import os
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials

try:
    with open("artists.json", "r") as f:
        artists = json.loads(f.read())
        f.close()
except EnvironmentError:
    artists = {}
    print("No artists.json file found")

spotify = spotipy.Spotify(client_credentials_manager=SpotifyClientCredentials())
changes = False

for artist, album_list in artists.items():
    results = spotify.artist_albums(artist)
    albums = results['items']
    while results['next']:
        results = spotify.next(results)
        albums.extend(results['items'])
    album_names = []
    for album in albums:
        album_names.append(album['name'])
    diff = set(album_names).difference(set(album_list))
    if diff != set():
        changes = True
        print("There are new albums by %s! %s"%(results['items'][0]['artists'][0]['name'], diff))
        album_list.extend(diff)
    artists.update({artist: album_list})

if changes:
    print("Updating artists.json")
    f = open("artists.json", "w")
    x = json.dumps(artists)
    f.write(x)
    f.close()