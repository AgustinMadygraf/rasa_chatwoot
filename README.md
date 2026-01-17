# rasa_chatwoot

Webhook minimo en FastAPI que escucha mensajes entrantes de Chatwoot y responde
con un mensaje fijo "Ok". Este proyecto es un esqueleto para luego integrar
con Rasa.

## Caracteristicas
- Valida un secreto compartido en la URL del webhook.
- Maneja solo eventos de mensajes entrantes.
- Publica una respuesta en la misma conversacion via la API de Chatwoot.

## Requisitos
- Python 3.10+ (recomendado)
- Cuenta de Chatwoot y un token de API de bot

## Instalacion
1) Crear un virtualenv e instalar dependencias:

```bash
python -m venv .venv
.\.venv\Scripts\activate
pip install -r requirements.txt
python.exe -m pip install --upgrade pip
```

2) Copiar el archivo de entorno y completar valores:

```bash
copy .env.example .env
```

Variables de entorno requeridas:
- `CHATWOOT_BASE_URL`: URL base de tu instancia de Chatwoot (sin slash final)
- `CHATWOOT_BOT_TOKEN`: Token de acceso API del bot
- `WEBHOOK_SECRET`: Secreto compartido usado en la URL del webhook

## Ejecucion

```bash
python run.py
```

El servicio escucha en `http://127.0.0.1:8000`.

## Produccion
Por ahora el punto de entrada es `run.py`. A futuro se puede reemplazar por un
comando de servidor (por ejemplo, uvicorn/gunicorn) segun el entorno.

## Webhook
Configura el webhook de Chatwoot asi:

```
http://your-host:8000/webhook/<WEBHOOK_SECRET>
```

El handler solo reacciona a:
- `event = message_created`
- `message_type = incoming`

Cuando llega un mensaje entrante valido, responde con `"Ok"`.

## Ejemplo de payload y respuesta
Payload (entrada desde Chatwoot, reducido):

```json
{
  "event": "message_created",
  "message_type": "incoming",
  "account": { "id": 1 },
  "conversation": { "id": 123 }
}
```

Respuesta (salida del webhook):

```json
{
  "ok": true,
  "status": 200,
  "detail": "..."
}
```

## Notas
- El cuerpo de respuesta esta fijo en `main.py`.
- Los errores de la API de Chatwoot se devuelven en la respuesta del webhook.
