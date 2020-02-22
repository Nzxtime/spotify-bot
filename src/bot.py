import spotipy
import spotipy.util as util
from twitchio.ext import commands
import json


class Bot(commands.Bot):
    with open('config.json') as config_file:
        data = json.load(config_file)

    scope = 'playlist-modify-public playlist-modify-private user-read-currently-playing user-read-playback-state ' \
            'user-modify-playback-state'
    token = util.prompt_for_user_token(username=data['spotify']['spotify_username'], scope=scope,
                                       client_id=data['spotify']['spotify_client_id'],
                                       client_secret=data['spotify']['spotify_client_secret'],
                                       redirect_uri=data['spotify']['spotify_redirect_uri'])

    def __init__(self):
        super().__init__(irc_token=self.data['twitch']['twitch_irc_token'],
                         client_id=self.data['twitch']['twitch_client_id'],
                         nick=self.data['twitch']['twitch_nick'], prefix=self.data['twitch']['twitch_prefix'],
                         initial_channels=self.data['twitch']['twitch_initial_channels'])
        self.disable_loop_and_shuffle()

    # Events don't need decorators when subclassed
    async def event_ready(self):
        print(f'Ready | {self.nick}')

    async def event_message(self, message):
        print(message.content)
        await self.handle_commands(message)

    @commands.command(name='song')
    async def song(self, ctx):
        result = self.get_current_track()
        await ctx.send(f'@{ctx.author.name} {result}')

    @commands.command(name='play')
    async def play(self, ctx, arg1):
        result = self.add_track_to_playlist(self.data['spotify']['spotify_username'],
                                            self.data['spotify']['spotify_playlist_id'], [arg1])
        await ctx.send(f'@{ctx.author.name} {result}')

    @commands.command(name='skip')
    async def skip(self, ctx):
        if ctx.message.tags['mod'] == 1 or str(ctx.author.name).lower() == str(ctx.message.channel).lower():
            result = self.skip_song()
            await ctx.send(f'@{ctx.author.name} {result}')
        else:
            await ctx.send(f'@{ctx.author.name}, you don\'t have the needed permission!')

    @commands.command(name='pl-clear')
    async def clear(self, ctx):
        if ctx.message.tags['mod'] == 1 or str(ctx.author.name).lower() == str(ctx.message.channel).lower():
            result = self.clear_playlist(self.data['spotify']['spotify_username'],
                                         self.data['spotify']['spotify_playlist_id'])
            await ctx.send(f'@{ctx.author.name} {result}')
        else:
            await ctx.send(f'@{ctx.author.name}, you don\'t have the needed permission!')

    @commands.command(name='dls')
    async def dls(self, ctx):
        if ctx.message.tags['mod'] == 1 or str(ctx.author.name).lower() == str(ctx.message.channel).lower():
            self.disable_loop_and_shuffle()
            await ctx.send(f'@{ctx.author.name} disabled loop and shuffle!')
        else:
            await ctx.send(f'@{ctx.author.name}, you don\'t have the needed permission!')

    def add_track_to_playlist(self, username, playlist_id, track_ids):
        if self.token:
            sp = spotipy.Spotify(auth=self.token)
            sp.trace = False
            results = sp.user_playlist_add_tracks(username, playlist_id, track_ids)
            print(results)
            return 'Added track'
        else:
            print('Getting new token')
            self.token['access_token'] = spotipy.SpotifyOAuth.get_access_token(spotipy.SpotifyOAuth())
            self.add_track_to_playlist(username, playlist_id, track_ids)

    def get_current_track(self):
        if self.token:
            sp = spotipy.Spotify(auth=self.token)
            sp.trace = False
            request = sp.current_user_playing_track()
            if request is not None:
                track = request['item']['name']
                artist = request['item']['artists'][0]['name']
                print(f'{track} - {artist}')
                return f'{track} - {artist}'
            else:
                print('Nothing playing at the moment...')
                return 'Nothing playing at the moment...'

        else:
            print('Getting new token')
            self.token['access_token'] = spotipy.SpotifyOAuth.get_access_token(spotipy.SpotifyOAuth())
            self.get_current_track()

    def clear_playlist(self, username, playlist_id):
        if self.token:
            sp = spotipy.Spotify(auth=self.token)
            sp.trace = False
            result = sp.playlist_tracks(playlist_id)
            tracks = []
            for i in result['items']:
                tracks.append(i['track']['uri'])
            results = sp.user_playlist_remove_all_occurrences_of_tracks(username, playlist_id, tracks)
            print(results)
            return 'Cleared playlist'
        else:
            print('Getting new token')
            self.token['access_token'] = spotipy.SpotifyOAuth.get_access_token(spotipy.SpotifyOAuth())
            self.clear_playlist(username, playlist_id)

    def skip_song(self):
        if self.token:
            sp = spotipy.Spotify(auth=self.token)
            sp.trace = False
            for device in sp.devices()['devices']:
                if device['is_active']:
                    results = sp.next_track(device_id=device['id'])
                    print(results)
            return 'Skipped song'
        else:
            print('Getting new token')
            self.token['access_token'] = spotipy.SpotifyOAuth.get_access_token(spotipy.SpotifyOAuth())
            self.skip_song()

    def disable_loop_and_shuffle(self):
        if self.token:
            sp = spotipy.Spotify(auth=self.token)
            sp.trace = False
            for device in sp.devices()['devices']:
                if device['is_active']:
                    sp.shuffle(False, device['id'])
                    sp.repeat('off', device['id'])
                    return
        else:
            print('Getting new token')
            self.token['access_token'] = spotipy.SpotifyOAuth.get_access_token(spotipy.SpotifyOAuth())
            self.disable_loop_and_shuffle()


bot = Bot()
bot.run()
