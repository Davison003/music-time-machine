import os
from dotenv import load_dotenv
load_dotenv("./.env")
SPOTIFY_ENDPOINT = os.getenv("SPOTIFY_ENDPOINT")
SPOTIFY_CLIENTID = os.getenv("CLIENT_ID")
SPOTIFY_SECRET = os.getenv("CLIENT_SECRET")

import spotipy
from spotipy.oauth2 import SpotifyOAuth
from spotipy.oauth2 import SpotifyClientCredentials

def spotipy_oauth(scope):
    return spotipy.Spotify(auth_manager=SpotifyOAuth(scope=scope,
                                                     client_id=SPOTIFY_CLIENTID,
                                                     client_secret=SPOTIFY_SECRET,
                                                     redirect_uri="http://example.com"))

def spotipy_cli_cred():
    return spotipy.Spotify(client_credentials_manager=SpotifyClientCredentials(
        client_id=SPOTIFY_CLIENTID,
        client_secret=SPOTIFY_SECRET))

def create_playlist(music_date):
    scope = "playlist-modify-public"
    sp = spotipy_oauth(scope)
    user_id = sp.me()['id']
    sp.user_playlist_create(user_id, f'25 hits from {music_date}',
                            description=f'Playlist created via Python script, '
                                        f'contains the "best" hits from {music_date}')


def add_songs_playlist(tracks, music_date):
    scope = 'playlist-modify-public'
    sp = spotipy_oauth(scope)
    playlist = [pl['uri'] for pl in sp.current_user_playlists()['items']
                if pl['name'] == f'25 hits from {music_date}']
    sp.playlist_add_items(playlist[0], tracks)


def search_track(song_details):
    sp = spotipy_cli_cred()
    result = sp.search(song_details)
    return result["tracks"]["items"][0]["uri"]