from dotenv import load_dotenv
import os

load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")
ADMIN_ID = os.getenv("ADMIN_ID")

YT_HEADERS_FILE = "headers_auth.json"
DATA_FILE = "data/tracks.json"

PORT = int(os.getenv("PORT", "10000"))

WEBHOOK_BASE_URL = (
    os.getenv("WEBHOOK_BASE_URL")
    or os.getenv("RENDER_EXTERNAL_URL")
)

if not BOT_TOKEN:
    raise ValueError("BOT_TOKEN is not set")