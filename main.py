import json
import os
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials, SpotifyOAuth

__location__ = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))

# TODO: Create installation script
# TODO: Port to ReactNative?
# TODO: Add fault tolerance
# TODO: Add automated testing
# TODO: Section into classes

# Note: We could look at artists followed by a user and automatically put them into the
#  artists.json file upon initialization using current_user_followed_artists

def artistLookup(spotify, artist_name):
    """Attempts to obtain the Spotify artist URI given a search term
    Examples:
     print(artistLookup(spotify, 'bad suns'))
     print(artistLookup(spotify, 'Good Kid'))
    """
    r = spotify.search(artist_name)
    for item in r['tracks']['items']:
        for artist in item['artists']:
            if artist_name.lower() == artist['name'].lower():
                return artist['uri']
    return None

# TODO: Create easier way for users to follow artists
def loadArtists():
    try:
        with open(os.path.join(__location__, "artists.json"), "r") as f:
            artists = json.loads(f.read())
            f.close()
    except EnvironmentError:
        artists = {}
        print("No artists.json file found")
    return artists

# TODO: Come up with a better solution than this
def loadEnvironment():
    try:
        with open(os.path.join(__location__, "spotify.config"), "r") as f:
            config = json.loads(f.read())
            os.environ['SPOTIPY_CLIENT_ID'] = config['SPOTIPY_CLIENT_ID']
            os.environ['SPOTIPY_CLIENT_SECRET'] = config['SPOTIPY_CLIENT_SECRET']
            os.environ['SPOTIPY_REDIRECT_URI'] = config['SPOTIPY_REDIRECT_URI']
            f.close()
    except EnvironmentError:
        print("No spotify config file found")
    return

def main():
    # Initialization
    artists = loadArtists()
    loadEnvironment()
    scope = "user-library-read user-library-modify"
    auth_manager = SpotifyOAuth(scope=scope)
    spotify = spotipy.Spotify(client_credentials_manager=SpotifyClientCredentials())
    spoauth = spotipy.Spotify(oauth_manager=auth_manager)
    changes = False

    # Get each artists' albums
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

        # If artist's albums differ from what we remembered...
        if diff != set():
            changes = True
            # TODO: Change how we notify the user of new content
            artist_name = spotify.artist(artist)['name']
            print("There are new albums by %s! %s"%(artist_name, diff))
            album_list.extend(diff)
            artists.update({artist: album_list})

    x = json.dumps(artists)
    # Update artists.json file if new albums are released
    if changes:
        f = open(os.path.join(__location__, "artists.json"), "w")
        f.write(x)
        f.close()
        input()         # Wait for user input so terminal doesn't close before user can read new albums
    return x

if __name__=="__main__":
    main()
