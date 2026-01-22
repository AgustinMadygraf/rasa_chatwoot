from fastapi import FastAPI, Request

from src.adapters.chatwoot_http import ChatwootHTTPAdapter
from src.domain.usecases.handle_incoming import HandleIncomingMessageUseCase
from src.controllers.webhook_controller import WebhookController

app = FastAPI()

adapter = ChatwootHTTPAdapter()
usecase = HandleIncomingMessageUseCase(adapter)
controller = WebhookController(usecase)


@app.post("/webhook/{secret}")
async def webhook(secret: str, request: Request):
    return await controller.handle(secret, request)
