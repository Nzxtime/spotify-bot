import spotipy
import spotipy.util as util
from twitchio.ext import commands
import json


class Bot(commands.Bot):
    with open('config.json') as config_file:
        data = json.load(config_file)

    scope = 'playlist-modify-public playlist-modify-private'
    token = util.prompt_for_user_token(data['spotify']['spotify_username'], scope)

    def __init__(self):
        super().__init__(irc_token=self.data['twitch']['twitch_irc_token'],
                         client_id=self.data['twitch']['twitch_client_id'],
                         nick=self.data['twitch']['twitch_nick'], prefix=self.data['twitch']['twitch_prefix'],
                         initial_channels=self.data['twitch']['twitch_initial_channels'])

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
        result = self.add_track_to_playlist(self.username, self.playlist_id, [arg1])
        await ctx.send(f'@{ctx.author.name} {result}')

    @commands.command(name='pl-clear')
    async def clear(self, ctx):
        if str(ctx.author.name).lower() == 'laserlord_':
            result = self.clear_playlist(self.username, self.playlist_id)
            await ctx.send(f'@{ctx.author.name} {result}')
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


bot = Bot()
bot.run()
