from typing import List, Sequence

from src.infrastructure.httpx.http_client import HttpxClient
from src.shared import config
from src.shared.logger import get_logger
from src.use_cases.rasa_gateway import RasaGateway

logger = get_logger(__name__)


class RasaHTTPGateway(RasaGateway):
    def __init__(self, base_url: str | None = None, client: HttpxClient | None = None, timeout: int = 10):
        self.base_url = base_url or config.RASA_REST_URL
        self.client = client or HttpxClient(timeout=timeout)

    async def send_message(self, sender_id: str, text: str) -> Sequence[str]:
        if not self.base_url:
            raise RuntimeError("RASA_REST_URL not set")
        body = {"sender": sender_id, "message": text}
        logger.info("Sending message to Rasa sender=%s", sender_id)
        status, resp_text = await self.client.post_json(self.base_url, headers={}, body=body)
        logger.debug("Rasa response status=%s body=%s", status, resp_text)

        if status >= 400:
            raise RuntimeError(f"Rasa error status={status}")

        # Rasa REST webhook returns a JSON list with objects that may contain 'text'
        try:
            import json

            data = json.loads(resp_text)
            if isinstance(data, list):
                texts: List[str] = []
                for item in data:
                    text_val = item.get("text") if isinstance(item, dict) else None
                    if text_val:
                        texts.append(str(text_val))
                return texts
        except Exception:
            logger.exception("Failed to parse Rasa response")

        return []
