import os

# Bot configuration
BOT_TOKEN = os.getenv("BOT_TOKEN")

if not BOT_TOKEN:
    raise ValueError("Éo thấy BOT_TOKEN")

ADMIN_ID = os.getenv("ADMIN_ID")

if not ADMIN_ID:
    raise ValueError("Éo thấy ADMIN_ID")
