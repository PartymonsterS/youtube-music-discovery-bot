from ytmusicapi import YTMusic


class YoutubeMusic:
    def __init__(self, headers_file: str):
        self.headers_file = headers_file
        self.client = None
        self.tracks = []

    def connect(self):
        self.client = YTMusic(self.headers_file)

    def get_liked_songs(self):
        if self.client is None:
            raise ValueError("Сначала вызови connect()")

        data = self.client.get_liked_songs(limit=5000)
        self.tracks = data.get("tracks", [])
        return self.tracks

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