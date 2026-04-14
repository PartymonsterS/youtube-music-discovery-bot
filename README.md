# 🎧 YouTube Music Discovery Bot

Telegram bot for music discovery using YouTube Music.

A lightweight tool to explore music in a fast, random, and engaging way.

---

## ⚠️ Note

Some features are **restricted to the bot owner**:
- 🎲 Random Track
- 🎶 Random Playlist
- ⚙️ Admin Panel

---

## ✨ Features

### 🎲 Random Track *(owner only)*
Shows a random track from liked songs.  
Useful for quick and effortless discovery from your personal library.

---

### 🎶 Random Playlist *(owner only)*
Builds a random playlist from liked songs.  
Great for generating instant mixes without thinking.

---

### 🔎 Search Playlist
Create a playlist based on:
- genre (phonk, jazz, techno)
- mood (sad, chill, aggressive)
- artist or style

---

### 🎧 Music Flow
Endless discovery mode:
1. Enter a query  
2. Get a track  
3. Continue with `Next`  

Feels like a simplified recommendation system.

---

### 📚 Playlist Discovery
Search public/community playlists by topic and browse them:
- gym phonk
- jazz night
- ambient piano

---

### ⚙️ Admin Panel *(owner only)*
Private bot controls:
- view settings
- sync data
- manage behavior

---

### 🗂 Configurable Settings
Stored in JSON:
- owner name
- playlist size
- search limits
- flow limits

---

## 🛠 Tech Stack

- Python
- aiogram (Telegram bot framework)
- ytmusicapi (YouTube Music API)
- python-dotenv
- JSON (lightweight storage)

---

## 📁 Project Structure

```text
project/
│
├── handlers/
├── keyboards/
├── states/
├── services/
├── data/
│
├── bot.py
├── config.py
├── main.py
├── youtube_music.py
├── requirements.txt
├── .env.example
└── .gitignore