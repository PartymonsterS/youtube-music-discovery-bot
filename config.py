from dotenv import load_dotenv
import os

load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")
ADMIN_ID = os.getenv("ADMIN_ID")


YT_HEADERS_FILE = "headers_auth.json"
DATA_FILE = "data/tracks.json"