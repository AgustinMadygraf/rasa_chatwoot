from typing import Any, Dict
from src.use_cases.chatwoot_gateway import ChatwootGateway
from src.shared.logger import get_logger

logger = get_logger(__name__)


class HandleIncomingMessageUseCase:
    def __init__(self, gateway: ChatwootGateway):
        self.gateway = gateway

    async def execute(self, payload: Dict[str, Any]) -> Dict[str, Any]:
        # Only react to incoming messages
        event = payload.get("event")
        msg_type = payload.get("message_type")
        logger.debug("Evaluating payload event=%s message_type=%s", event, msg_type)
        if event != "message_created" or msg_type != "incoming":
            logger.debug("Ignoring non-incoming or non-message_created event")
            return {"ok": True}

        account_id = (payload.get("account") or {}).get("id")
        conversation_id = (payload.get("conversation") or {}).get("id")

        logger.debug("Parsed account_id=%s conversation_id=%s", account_id, conversation_id)

        if not account_id or not conversation_id:
            logger.warning("Missing account_id or conversation_id in payload")
            return {"ok": False, "error": "missing account_id or conversation_id"}

        content = "Ok"
        logger.info("Sending reply content='%s' to account=%s conv=%s", content, account_id, conversation_id)

        try:
            status, text = await self.gateway.send_message(account_id, conversation_id, content)
        except Exception as e:
            logger.exception("Error sending message via gateway: %s", e)
            return {"ok": False, "error": "request error", "detail": str(e)}

        logger.info("Chatwoot response status=%s", status)
        logger.debug("Chatwoot response body=%s", text)

        return {"ok": status < 400, "status": status, "detail": text}
