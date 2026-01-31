import os

# Chatwoot configuration read from environment
CHATWOOT_BASE_URL = os.getenv("CHATWOOT_BASE_URL", "").rstrip("/")
CHATWOOT_BOT_TOKEN = os.getenv("CHATWOOT_BOT_TOKEN", "")
WEBHOOK_SECRET = os.getenv("WEBHOOK_SECRET", "")
LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO").upper()
URL_WEBHOOK = os.getenv("URL_WEBHOOK", "")
PORT = int(os.getenv("PORT", "8000"))
RELOAD = os.getenv("RELOAD", "0") == "1"
BRIDGE_HOST = "127.0.0.1"

# Rasa settings (hardcoded, no env)
RASA_BASE_URL = "http://localhost:5005"
RASA_REST_URL = f"{RASA_BASE_URL}/webhooks/rest/webhook"
