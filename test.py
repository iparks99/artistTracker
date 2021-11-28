import json, os, spotipy
from spotipy.oauth2 import SpotifyOAuth
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


scope = "user-follow-read user-library-modify"

sp = spotipy.Spotify(auth_manager=SpotifyOAuth(scope=scope))

results = sp.current_user_followed_artists()
for idx, artist in enumerate(results['artists']['items']):
    print(idx, artist['name'] + " - " + artist['uri'])

me = sp.me()
print(me)
