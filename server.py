import json, os, spotipy
from flask import Flask, render_template, request
from spotipy.oauth2 import SpotifyClientCredentials
app = Flask(__name__)
__location__ = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))

try:
    with open(os.path.join(__location__, "spotify.config"), "r") as f:
        config = json.loads(f.read())
        os.environ['SPOTIPY_CLIENT_ID'] = config['SPOTIPY_CLIENT_ID']
        os.environ['SPOTIPY_CLIENT_SECRET'] = config['SPOTIPY_CLIENT_SECRET']
        f.close()
except EnvironmentError:
    print("No spotify config file found")
spotify = spotipy.Spotify(client_credentials_manager=SpotifyClientCredentials())

@app.route('/followedartists', methods=['GET', 'POST'])
def renderFollowedArtists():
    if request.method == 'GET':
        return render_template('index.html')
    try:
        with open(os.path.join(__location__, "artists.json"), "r") as f:
            artists = json.loads(f.read())
            f.close()
            r = spotify.artists(artists)
            return r
    except EnvironmentError:
        return "Error: Could not open artists.json"

@app.route('/viewartist/albums', methods=['GET', 'POST'])
def renderViewArtistAlbums():
    if request.method == 'GET':
        return render_template('index.html')
    if 'artisturi' in request.form:
        uri = request.form.get('artisturi')
        r = spotify.artist_albums(uri)
        return r
    else:
        return "Error: no artist uri given"

@app.route('/viewartist', methods=['GET', 'POST'])
def renderViewArtist():
    if request.method == 'GET':
        return render_template('index.html')
    if 'artisturi' in request.form:
        uri = request.form.get('artisturi')
        r = spotify.artist(uri)
        return r
    else:
        return "Error: No artist uri given"

@app.route('/search', methods=['GET', 'POST'])
def renderSearch():
    if request.method == 'GET':
        return render_template('index.html')
    if 'artistname' in request.form:
        artist_name = request.form.get('artistname')
        r = spotify.search(artist_name, type='artist')
        # print(r['artists'])
        return r['artists']
    else:
        return "Error: No artist name entered"

@app.route('/')
def display():
    return render_template('index.html')

if __name__=='__main__':
    app.run(port=8888)