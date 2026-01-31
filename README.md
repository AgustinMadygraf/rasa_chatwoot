# rasa_chatwoot

Servicio FastAPI con un webhook que recibe eventos de Chatwoot y responde usando Chatwoot,
con integracion opcional a Rasa. Incluye scripts para correr Rasa, entrenar y abrir tunel ngrok.

## Que hace
- Expone un endpoint `POST /webhook/{secret}`.
- Valida el secreto recibido contra `WEBHOOK_SECRET`.
- Para eventos `message_created` con `message_type = incoming`, envia una respuesta a Chatwoot.
- Si Rasa devuelve textos, usa el primero; si falla o no hay respuesta, responde `"Bot no activado"`.
- Si no hay contenido entrante, responde `"Ok"`.

## Requisitos
- Python 3.10+

## Instalacion
```bash
python -m venv .venv
.\.venv\Scriptsctivate
pip install -r requirements.txt
```

## Variables de entorno
- `CHATWOOT_BASE_URL`
- `CHATWOOT_BOT_TOKEN`
- `WEBHOOK_SECRET`
- `LOG_LEVEL`
- `PORT` (default 8000)
- `RELOAD` (default "0")
- `URL_WEBHOOK` (para ngrok)

## Rasa
- `RASA_BASE_URL` esta hardcodeado en `src/shared/config.py` como `http://localhost:5005`.
- El proyecto Rasa vive en `src/infrastructure/rasa` (config.yml, domain.yml, data/, models/).

## Entrypoints
```bash
python run_chatwoot_rasa_bridge.py
python run_rasa_server.py
python run_rasa_train.py
python run_ngrok_tunnel.py
```

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
- Se recomienda ejecutar Uvicorn/Gunicorn directamente contra
  `src.interface_adapter.presenters.webhook_api:app`.
