from ytmusicapi import YTMusic
import random
import json
from config import YT_HEADERS_FILE


class YoutubeMusic:

    def __init__(self, headers_file: str):
        self.headers_file = headers_file
        self.client = None
        self.data_file = "data/tracks.json"

    def connect(self):
        self.client = YTMusic(self.headers_file)

    def load_tracks(self):
        try:
            with open(self.data_file, "r", encoding="utf-8") as f:
                return json.load(f)
        except FileNotFoundError:
            return []

    def save_tracks(self, tracks):
        with open(self.data_file, "w", encoding="utf-8") as f:
            json.dump(tracks, f, ensure_ascii=False, indent=2)

    def full_sync(self):
        if self.client is None:
            raise ValueError("Сначала вызови connect()")

        data = self.client.get_liked_songs(limit=5000)
        tracks = data.get("tracks", [])

        self.save_tracks(tracks)

        return {
            "mode": "full_sync",
            "total": len(tracks)
        }

    def sync_new(self):
        if self.client is None:
            raise ValueError("Сначала вызови connect()")

        old_tracks = self.load_tracks()

        old_ids = {
            track.get("videoId")
            for track in old_tracks
            if track.get("videoId")
        }

        data = self.client.get_liked_songs(limit=5000)
        fresh_tracks = data.get("tracks", [])

        new_tracks = []

        for track in fresh_tracks:
            video_id = track.get("videoId")

            if video_id and video_id not in old_ids:
                new_tracks.append(track)

        updated_tracks = old_tracks + new_tracks

        self.save_tracks(updated_tracks)

        return {
            "mode": "sync_new",
            "added": len(new_tracks),
            "total": len(updated_tracks)
        }

    def get_liked_songs(self):
        return self.load_tracks()

    def get_liked_random(self):
        tracks = self.load_tracks()

        if not tracks:
            raise ValueError("Нет треков. Сначала сделай /sync")

        return random.choice(tracks)

    def get_tracks_count(self):
        return len(self.load_tracks())

    def preview_tracks(self, limit=5):
        tracks = self.load_tracks()
        preview = []

        for track in tracks[:limit]:
            title = track.get("title", "Unknown title")
            artists = track.get("artists", [])

            if artists:
                artist_name = artists[0].get("name", "Unknown artist")
            else:
                artist_name = "Unknown artist"

            preview.append(f"{artist_name} — {title}")

        return preview

    def search_tracks(self, query: str, limit: int = 20):
        if self.client is None:
            raise ValueError("Сначала вызови connect()")

        songs = self.client.search(query, filter="songs", limit=limit * 2)
        videos = self.client.search(query, filter="videos", limit=limit * 2)

        results = songs + videos

        tracks = []
        seen_ids = set()

        for item in results:
            video_id = item.get("videoId")
            if not video_id or video_id in seen_ids:
                continue

            title = item.get("title", "Unknown title")
            artists = item.get("artists", [])

            if artists:
                artist_name = artists[0].get("name", "Unknown artist")
            else:
                artist_name = "Unknown artist"

            tracks.append({
                "title": title,
                "artist": artist_name,
                "videoId": video_id,
                "url": f"https://music.youtube.com/watch?v={video_id}"
            })

            seen_ids.add(video_id)

            if len(tracks) >= limit:
                break

        return tracks

ym_client = YoutubeMusic(YT_HEADERS_FILE)