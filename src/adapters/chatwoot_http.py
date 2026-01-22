import httpx
from typing import Tuple
from src.ports.chatwoot_gateway import ChatwootGateway
from src.shared import config
from src.shared.logger import get_logger

logger = get_logger(__name__)


class ChatwootHTTPAdapter(ChatwootGateway):
    def __init__(self, base_url: str | None = None, token: str | None = None, timeout: int = 10):
        self.base_url = base_url or config.CHATWOOT_BASE_URL
        self.token = token or config.CHATWOOT_BOT_TOKEN
        self.timeout = timeout

    async def send_message(self, account_id: int, conversation_id: int, content: str) -> Tuple[int, str]:
        if not self.base_url:
            raise RuntimeError("CHATWOOT_BASE_URL not set")
        url = f"{self.base_url}/api/v1/accounts/{account_id}/conversations/{conversation_id}/messages"
        headers = {"api_access_token": self.token}
        body = {"content": content, "message_type": "outgoing"}

        logger.info("Sending message to Chatwoot %s", url)
        logger.debug("Request headers=%s body=%s", headers, body)
        try:
            async with httpx.AsyncClient(timeout=self.timeout) as client:
                resp = await client.post(url, headers=headers, json=body)
        except httpx.RequestError as e:
            logger.exception("HTTP request error when sending to Chatwoot: %s", e)
            raise
        except Exception as e:
            logger.exception("Unexpected error when sending to Chatwoot: %s", e)
            raise

        # Truncate response text for debug if very large
        resp_text = resp.text
        if isinstance(resp_text, str) and len(resp_text) > 1000:
            logger.debug("Chatwoot response (truncated): %s", resp_text[:1000])
        else:
            logger.debug("Chatwoot response body: %s", resp_text)

        logger.info("Chatwoot returned status=%s", resp.status_code)
        return resp.status_code, resp_text
