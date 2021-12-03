import spotipy
from spotipy.oauth2 import SpotifyOAuth
from twitchio.ext import commands
import json
from os import path


class Bot():
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

    def add_track_to_playlist(self, username, playlist_id, track_ids):
        self.sp.trace = False
        results = self.sp.playlist_add_items(username, playlist_id, track_ids)
        print(results)
        return 'Added track'

    def get_current_track(self):
        self.sp.trace = False
        request = self.sp.current_user_playing_track()
        if request is not None:
            track = request['item']['name']
            artist = request['item']['artists'][0]['name']
            print(f'{track} - {artist}')
            return f'{track} - {artist}'
        else:
            print('Nothing playing at the moment...')
            return 'Nothing playing at the moment...'

    def clear_playlist(self, username, playlist_id):
        self.sp.trace = False
        result = self.sp.playlist_tracks(playlist_id)
        tracks = []
        for i in result['items']:
            tracks.append(i['track']['uri'])
        results = self.sp.user_playlist_remove_all_occurrences_of_tracks(username, playlist_id, tracks)
        print(results)
        return 'Cleared playlist'

    def skip_song(self):
        self.sp.trace = False
        for device in self.sp.devices()['devices']:
            if device['is_active']:
                results = self.sp.next_track(device_id=device['id'])
                print(results)
        return 'Skipped song'

    def disable_loop_and_shuffle(self):
        self.sp.trace = False
        for device in self.sp.devices()['devices']:
            if device['is_active']:
                self.sp.shuffle(False, device['id'])
                self.sp.repeat('off', device['id'])
                return


bot = Bot()
