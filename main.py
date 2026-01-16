import os
from fastapi import FastAPI, Request, HTTPException
import httpx
from dotenv import load_dotenv

load_dotenv()  # lee .env

app = FastAPI()

CHATWOOT_BASE_URL = os.getenv("CHATWOOT_BASE_URL", "").rstrip("/")
CHATWOOT_BOT_TOKEN = os.getenv("CHATWOOT_BOT_TOKEN", "")
WEBHOOK_SECRET = os.getenv("WEBHOOK_SECRET", "")

@app.post("/webhook/{secret}")
async def webhook(secret: str, request: Request):
    if secret != WEBHOOK_SECRET:
        raise HTTPException(status_code=401, detail="unauthorized")

    payload = await request.json()

    # Solo reaccionar a mensajes entrantes
    if payload.get("event") != "message_created" or payload.get("message_type") != "incoming":
        return {"ok": True}

    account_id = (payload.get("account") or {}).get("id")
    conversation_id = (payload.get("conversation") or {}).get("id")

    if not account_id or not conversation_id:
        return {"ok": False, "error": "missing account_id or conversation_id"}

    if not CHATWOOT_BASE_URL:
        return {"ok": False, "error": "CHATWOOT_BASE_URL not set"}

    url = f"{CHATWOOT_BASE_URL}/api/v1/accounts/{account_id}/conversations/{conversation_id}/messages"
    headers = {"api_access_token": CHATWOOT_BOT_TOKEN}
    body = {"content": "Ok", "message_type": "outgoing"}

    try:
        async with httpx.AsyncClient(timeout=10) as client:
            resp = await client.post(url, headers=headers, json=body)
    except httpx.RequestError as e:
        return {"ok": False, "error": "request error", "detail": str(e)}
    except Exception as e:
        return {"ok": False, "error": "unexpected error", "detail": str(e)}

    return {"ok": resp.status_code < 400, "status": resp.status_code, "detail": resp.text}
