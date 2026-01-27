# rasa_chatwoot

Servicio FastAPI con un webhook que recibe eventos de Chatwoot y responde usando Chatwoot, con integracion opcional a Rasa.

## Que hace
- Expone un endpoint `POST /webhook/{secret}`.
- Valida el secreto recibido contra `WEBHOOK_SECRET`.
- Para eventos `message_created` con `message_type = incoming`, envia una respuesta a Chatwoot.
- Si hay Rasa configurado y devuelve textos, usa el primer texto; si falla o no hay respuesta, responde con `"Bot no activado"`.
- Si no hay Rasa o no hay contenido entrante, responde con `"Ok"`.

## Requisitos
- Python 3.10+

## Instalacion
```bash
python -m venv .venv
.\.venv\Scripts\activate
pip install -r requirements.txt
```

## Variables de entorno leidas
- `CHATWOOT_BASE_URL`
- `CHATWOOT_BOT_TOKEN`
- `WEBHOOK_SECRET`
- `LOG_LEVEL`
- `URL_WEBHOOK`
- `RASA_REST_URL` (default: `http://localhost:5005/webhooks/rest/webhook`)

## Ejecucion local
```bash
python run.py
```

`run.py` levanta Uvicorn en `127.0.0.1` y usa:
- `PORT` (default 8000)
- `RELOAD` (default "0")

## Webhook en Chatwoot
Configura el webhook con esta URL:

```
http://<host>:8000/webhook/<WEBHOOK_SECRET>
```

El handler solo reacciona a:
- `event = message_created`
- `message_type = incoming`

## Payload esperado (ejemplo)
```json
{
  "event": "message_created",
  "message_type": "incoming",
  "account": { "id": 1 },
  "conversation": { "id": 123 },
  "content": "Hola"
}
```

## Respuesta del webhook (ejemplo)
```json
{
  "ok": true,
  "status": 200,
  "detail": "..."
}
```

## Produccion
- El punto de entrada actual es `run.py`.
- Para produccion, se recomienda ejecutar Uvicorn/Gunicorn directamente contra `src.interface_adapter.presenters.webhook_api:app`.
