import os
from dotenv import load_dotenv
load_dotenv("./.env")

SPOTIFY_CLIENTID = os.getenv("CLIENT_ID")
SPOTIFY_SECRET = os.getenv("CLIENT_SECRET")

import spotipy
from spotipy.oauth2 import SpotifyOAuth
from spotipy.oauth2 import SpotifyClientCredentials

class SpotipyManager:
    def __init__(self, music_date):
        self.client_id = SPOTIFY_CLIENTID
        self.client_secret = SPOTIFY_SECRET
        self.redirect = "http://example.com"
        self.user_date = music_date

    def spotipy_oauth(self, scope):
        return spotipy.Spotify(auth_manager=SpotifyOAuth(scope=scope,
                                                         client_id=self.client_id,
                                                         client_secret=self.client_secret,
                                                         redirect_uri=self.redirect))

    def spotipy_cli_cred(self):
        return spotipy.Spotify(client_credentials_manager=SpotifyClientCredentials(
            client_id=self.client_id,
            client_secret=self.client_secret))

    def search_track(self, song_details):
        sp = self.spotipy_cli_cred()
        result = sp.search(song_details)
        return result["tracks"]["items"][0]["uri"]


    def create_playlist(self):
        scope = "playlist-modify-public"
        sp = self.spotipy_oauth(scope)
        user_id = sp.me()['id']
        sp.user_playlist_create(user_id, f'25 hits from {self.user_date}',
                                description=f'Playlist created via Python script, '
                                            f'contains the "best" hits from {self.user_date}')

    def add_songs_playlist(self, tracks):
        scope = 'playlist-modify-public'
        sp = self.spotipy_oauth(scope)
        playlist = [pl['uri'] for pl in sp.current_user_playlists()['items']
                    if pl['name'] == f'25 hits from {self.user_date}']
        sp.playlist_add_items(playlist[0], tracks)


