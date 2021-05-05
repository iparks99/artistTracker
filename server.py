import json, os, spotipy, time
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

@app.route('/followedartists/follow', methods=['GET', 'POST'])
def renderFollowArtist():
    if request.method == 'GET':
        return render_template('index.html')
    if 'artisturi' not in request.form:
        return "Error: no artist uri given"
    uri = request.form.get('artisturi')
    r = spotify.artist(uri)
    if 'error' in r:
        return "Error: Invalid artist uri"
    try:
        with open(os.path.join(__location__, "artists.json"), "r+") as f:
            print("[follow] opened artists.json")
            artists = json.loads(f.read())
            f.seek(0)
            # f.close()
            # print("[follow] closed artists.json")
            if uri in artists:
                return "Error: Already following artist"
            else:
                artists[uri] = []
            x = json.dumps(artists)
            # f = open(os.path.join(__location__, "artists.json"), "w")
            # print("[follow] opened artists.json")
            f.write(x)
            f.truncate()
            f.close()
            print("[follow] closed artists.json")
            # print('/followedartists/follow: %s'%artists)
            return "Success"
    except EnvironmentError:
        return "Error: Could not follow artist"

@app.route('/followedartists/unfollow', methods=['GET', 'POST'])
def renderUnfollowArtist():
    if request.method == 'GET':
        return render_template('index.html')
    if 'artisturi' not in request.form:
        return "Error: no artist uri given"
    uri = request.form.get('artisturi')
    try:
        with open(os.path.join(__location__, "artists.json"), "r+") as f:
            print("[unfollow] opened artists.json")
            artists = json.loads(f.read())
            f.seek(0)
            # print("[unfollow] closed artists.json")
            if uri not in artists:
                return "Error: User not following artist"
            else:
                del artists[uri]
                x = json.dumps(artists)
                # f = open(os.path.join(__location__, "artists.json"), "w")
                # print("[unfollow] opened artists.json")
                f.write(x)
                f.truncate()
                f.close()
                print("[unfollow] closed artists.json")
                return "Success"
    except EnvironmentError:
        return "Error: Could not unfollow artist"

@app.route('/followedartists', methods=['GET', 'POST'])
def renderFollowedArtists():
    if request.method == 'GET':
        return render_template('index.html')
    try:
        time.sleep(0.1)
        with open(os.path.join(__location__, "artists.json"), "r") as f:
            print("[sidenav] opened artists.json")
            artists = json.loads(f.read())
            # print('/followedartists: %s'%artists)
            f.close()
            print("[sidenav] closed artists.json")
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