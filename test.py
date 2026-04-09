from ytmusicapi import YTMusic

yt = YTMusic("headers_auth.json")

data = yt.get_liked_songs(limit=20)

print(len(data["tracks"]))
print(data["tracks"][0]["title"])

for track in data["tracks"]:
    print(track["title"])