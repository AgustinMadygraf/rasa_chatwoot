from fastapi import FastAPI, Request

from src.interface_adapter.gateways.chatwoot_http import ChatwootHTTPAdapter
from src.use_cases.handle_incoming import HandleIncomingMessageUseCase
from src.interface_adapter.controller.webhook_controller import WebhookController

app = FastAPI()

adapter = ChatwootHTTPAdapter()
usecase = HandleIncomingMessageUseCase(adapter)
controller = WebhookController(usecase)


@app.post("/webhook/{secret}")
async def webhook(secret: str, request: Request):
    return await controller.handle(secret, request)
