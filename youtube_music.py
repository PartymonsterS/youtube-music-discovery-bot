from ytmusicapi import YTMusic
import random
from config import YT_HEADERS_FILE
class YoutubeMusic:
    def __init__(self, headers_file: str):
        self.headers_file = headers_file
        self.client = None
        self.tracks = []
        self.tracks_data = {}

    def connect(self):
        self.client = YTMusic(self.headers_file)

    def sync_tracks(self):
        self.tracks_data = self.client.get_liked_songs(limit=100)
        self.tracks = self.tracks_data['tracks']

    def get_liked_songs(self):
        return self.tracks

    def get_liked_random_song(self):
        return random.choice(self.tracks)

    def get_tracks_count(self):
        return len(self.tracks)

    def preview_tracks(self, limit=5):
        preview = []

        for track in self.tracks[:limit]:
            title = track.get("title", "Unknown title")
            artists = track.get("artists", [])

            if artists:
                artist_name = artists[0].get("name", "Unknown artist")
            else:
                artist_name = "Unknown artist"

            preview.append(f"{artist_name} — {title}")

        return preview


ym_client = YoutubeMusic(YT_HEADERS_FILE)