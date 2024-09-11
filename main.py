import  requests, re
from datetime import datetime
from bs4 import BeautifulSoup

from spotipy_manager import create_playlist, search_track, add_songs_playlist
BILLBOARD_URL = "https://www.billboard.com/charts/hot-100/"

music_date = input("Desired date (YYYY-MM-DD): ")
is_date_valid = True

try:
    correct_format = "%Y-%m-%d"
    is_date_valid = bool(datetime.strptime(music_date, correct_format))
except ValueError:
    is_date_valid = False

if is_date_valid:
    res = requests.get(f"{BILLBOARD_URL}{music_date}/")
    res.raise_for_status()
    soup = BeautifulSoup(res.text, 'html.parser')

    songs_elements = soup.select(selector=".o-chart-results-list-row-container")

    create_playlist(music_date)
    songs_info = []
    for el in songs_elements:
        info_title = el.select_one("li>h3#title-of-a-story")
        info_artist = el.select_one("li>h3 + span")

        title_stripped = re.sub('\s+', ' ', info_title.string)
        artist_stripped = re.sub('\s+', ' ', info_artist.string)

        songs_info.append(f"{title_stripped} {artist_stripped}")

    list_tracks = [search_track(song) for song in songs_info]
    add_songs_playlist(list_tracks[:25], music_date)
