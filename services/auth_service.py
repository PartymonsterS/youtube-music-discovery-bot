import json
from pathlib import Path


YT_AUTH_PATH = Path("data/yt_auth.json")


def load_yt_auth() -> dict:
    with open(YT_AUTH_PATH, "r", encoding="utf-8") as f:
        return json.load(f)


def save_yt_auth(auth_data: dict) -> None:
    with open(YT_AUTH_PATH, "w", encoding="utf-8") as f:
        json.dump(auth_data, f, ensure_ascii=False, indent=4)


def get_yt_auth_value(key: str):
    auth_data = load_yt_auth()
    return auth_data.get(key)


def set_yt_auth_value(key: str, value: str) -> None:
    auth_data = load_yt_auth()
    auth_data[key] = value
    save_yt_auth(auth_data)