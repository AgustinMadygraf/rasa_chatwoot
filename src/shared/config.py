import os
from dotenv import load_dotenv

load_dotenv()

# Chatwoot configuration read from environment
CHATWOOT_BASE_URL = os.getenv("CHATWOOT_BASE_URL", "").rstrip("/")
CHATWOOT_BOT_TOKEN = os.getenv("CHATWOOT_BOT_TOKEN", "")
WEBHOOK_SECRET = os.getenv("WEBHOOK_SECRET", "")
LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO").upper()
