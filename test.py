from ytmusicapi import YTMusic
from config import YT_HEADERS_FILE

yt = YTMusic(YT_HEADERS_FILE)

query = "gym phonk"

results = yt.search(query, limit=20)

for i, item in enumerate(results, start=1):
    print(f"\n--- {i} ---")
    print("title:", item.get("title"))
    print("resultType:", item.get("resultType"))
    print("playlistId:", item.get("playlistId"))
    print("videoId:", item.get("videoId"))
    print("author:", item.get("author"))
    print("itemCount:", item.get("itemCount"))
    print("raw:", item)