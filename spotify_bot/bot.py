import spotipy
from spotipy.oauth2 import SpotifyOAuth
from twitchio.ext import commands
import json
from os import path


class Bot(commands.Bot):
    for location in path.expanduser("~/.config/spotify-bot/"), "/etc/spotify-bot/":
        try:
            print(path.join(location, "config.json"))
            with open(path.join(location, "config.json")) as source:
                data = json.load(source)
        except IOError:
            pass

    if data is None:
        print('Create a config.json file in the following directory:')
        print(path.abspath(path.expanduser("~/.config/spotify-bot/")) + ' or /etc/spotify-bot/')
        print('Use the config.json.example as a reference.')
        print('For further information visit https://github.com/Nzxtime/spotify-bot')
        exit()

    scope = 'playlist-modify-public playlist-modify-private user-read-currently-playing user-read-playback-state ' \
            'user-modify-playback-state'

    sp = spotipy.Spotify(auth_manager=SpotifyOAuth(scope=scope,
                                                   client_id=data['spotify']['spotify_client_id'],
                                                   client_secret=data['spotify']['spotify_client_secret'],
                                                   redirect_uri=data['spotify']['spotify_redirect_uri']))

