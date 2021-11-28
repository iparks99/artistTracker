import base64, json, os, requests, spotipy, time
from flask import Flask, redirect, render_template, request, url_for
from spotipy.oauth2 import SpotifyClientCredentials, SpotifyOAuth
app = Flask(__name__)
__location__ = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))

try:
    with open(os.path.join(__location__, "spotify.config"), "r") as f:
        config = json.loads(f.read())
        os.environ['SPOTIPY_CLIENT_ID'] = config['SPOTIPY_CLIENT_ID']
        os.environ['SPOTIPY_CLIENT_SECRET'] = config['SPOTIPY_CLIENT_SECRET']
        os.environ['SPOTIPY_REDIRECT_URI'] = config['SPOTIPY_REDIRECT_URI']
        f.close()
except EnvironmentError:
    print("No spotify config file found")
scope = "user-library-read user-library-modify"
cache_path = ".cache"
spotify = spotipy.Spotify(client_credentials_manager=SpotifyClientCredentials())
auth_manager = SpotifyOAuth(scope=scope)
spoauth = spotipy.Spotify(oauth_manager=auth_manager)

@app.route('/callback', methods=['GET', 'POST'])
def callback():
    # if request.method == 'GET':
    #     data = request.args
    #     if 'code' in data:
    #         # Get the code from the url
    #         code = data['code']

    #         # Get the client ID and secret from the environment
    #         client_id = os.environ['SPOTIPY_CLIENT_ID']
    #         client_secret = os.environ['SPOTIPY_CLIENT_SECRET']

    #         # Forming the header and payload
    #         header = client_id + ':' + client_secret
    #         headStr = str(base64.b64encode(header.encode('utf-8')), "utf-8")
    #         headers = { 'Authorization' : 'Basic ' + headStr }
    #         payload = { 'grant_type' : 'authorization_code', 'code' : code, 'redirect_uri' : 'http://localhost:8888/callback' }

    #         # Sending post request to obtain access and refresh tokens
    #         r = requests.post('https://accounts.spotify.com/api/token', data = payload, headers = headers)

    #         # Parsing response as a JSON object
    #         response = json.loads(r.text)

    #         # Extracting access and refresh tokens
    #         access_token = response['access_token']
    #         refresh_token = response['refresh_token']
    #         expires_in = response['expires_in']
    #         print('access token: ' + access_token)
    #         print('refresh token: ' + refresh_token)
    #         print('expires in: ' + str(expires_in))

    #         # Using access token to access api
    #         headers = { 'Authorization' : 'Bearer ' + access_token }
    #         r = requests.get('https://api.spotify.com/v1/me', headers = headers)
    #         print(json.loads(r.text))
    #     else:
    #         return 'Error: No code given in OAuth process'
    print("in callback")
    # render_template('index.html')
    return redirect(url_for('display'))
    # return render_template('index.html')

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
            artists = json.loads(f.read())
            f.seek(0)
            if uri in artists:
                return "Error: Already following artist"
            else:
                artists[uri] = []
            x = json.dumps(artists)
            f.write(x)
            f.truncate()
            f.close()
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
            artists = json.loads(f.read())
            f.seek(0)
            if uri not in artists:
                return "Error: User not following artist"
            else:
                del artists[uri]
                x = json.dumps(artists)
                f.write(x)
                f.truncate()
                f.close()
                return "Success"
    except EnvironmentError:
        return "Error: Could not unfollow artist"

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
        return r['artists']
    else:
        return "Error: No artist name entered"

@app.route('/')
def display():
    access_token = get_cached_token()
    print(access_token)

    if access_token:
        return render_template('index.html')
    else:
        auth_url = auth_manager.get_authorize_url()
        htmlLoginButton = "<a href='" + auth_url + "'>Login to Spotify</a>"
        return htmlLoginButton

def get_cached_token(filename=cache_path, as_dict=False):
    """Obtains the cached access token, if one exists, in a given file.
    File defaults to cache path
    Returns None if one does not exist, file does not exist or cannot
    be opened, or if it is expired.
    """
    try:
        with open(os.path.join(__location__, filename), "r") as f:
            token_info = json.loads(f.read())
            f.close()
            if token_info['access_token'] and token_info['expires_at']:
                if int(time.time()) < token_info['expires_at']:
                    if as_dict:
                        return token_info
                    else:
                        return token_info['access_token']
    except:
        return None

if __name__=='__main__':
    app.run(port=8888)