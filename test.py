import json

with open("data.json", "r", encoding="utf-8") as f:
    tracks = json.load(f)

seen = set()
duplicates = []

for i, track in enumerate(tracks, start=1):

    title = track.get("title", "Unknown title")
    video_id = track.get("videoId")

    print(f"{i}. {title}")

    if video_id in seen:
        duplicates.append(video_id)
    else:
        seen.add(video_id)

print("\nВсего треков:", len(tracks))
print("Уникальных videoId:", len(seen))

if duplicates:
    print("Найдены дубликаты:", len(duplicates))
else:
    print("Дубликатов нет ✅")

