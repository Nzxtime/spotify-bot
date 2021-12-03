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

    def add_track_to_playlist(self, playlist_id, track_ids):
        self.sp.trace = False
        results = self.sp.playlist_add_items(playlist_id, track_ids)
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

    def __init__(self):
        super().__init__(token=self.data['twitch']['twitch_access_token'],
                         prefix=self.data['twitch']['twitch_prefix'],
                         initial_channels=self.data['twitch']['twitch_initial_channels'])

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
        result = self.add_track_to_playlist(self.data['spotify']['spotify_playlist_id'], [arg1])
        await ctx.send(f'@{ctx.author.name} {result}')

    @commands.command(name='skip')
    async def skip(self, ctx):
        if ctx.author.is_mod or str(ctx.author.name).lower() == str(ctx.message.channel).lower():
            result = self.skip_song()
            await ctx.send(f'@{ctx.author.name} {result}')
        else:
            await ctx.send(f'@{ctx.author.name}, you don\'t have the needed permission!')

    @commands.command(name='clear')
    async def clear(self, ctx):
        if ctx.author.is_mod or str(ctx.author.name).lower() == str(ctx.message.channel).lower():
            result = self.clear_playlist(self.data['spotify']['spotify_username'],
                                         self.data['spotify']['spotify_playlist_id'])
            await ctx.send(f'@{ctx.author.name} {result}')
        else:
            await ctx.send(f'@{ctx.author.name}, you don\'t have the needed permission!')

    @commands.command(name='dls')
    async def dls(self, ctx):
        if ctx.author.is_mod or str(ctx.author.name).lower() == str(ctx.message.channel).lower():
            self.disable_loop_and_shuffle()
            await ctx.send(f'@{ctx.author.name} disabled loop and shuffle!')
        else:
            await ctx.send(f'@{ctx.author.name}, you don\'t have the needed permission!')

    @commands.command(name='help')
    async def dls(self, ctx):
        await ctx.send(f'@{ctx.author.name} song, play, skip, clear, dls, queue')

    @commands.command(name='queue')
    async def queue(self, ctx):
        await ctx.send(
            f'@{ctx.author.name} https://open.spotify.com/playlist/{self.data["spotify"]["spotify_playlist_id"]}')


bot = Bot()
bot.run()
