import httpx
import logging
import asyncio
from config import settings

logger = logging.getLogger(__name__)

async def send_webhook(webhook_url: str, payload: dict):
    try:
        async with httpx.AsyncClient(timeout=10) as client:
            response = await client.post(webhook_url, json=payload)
            response.raise_for_status()
            logger.info(f"Webhook sent to {webhook_url}")
            return True
    except httpx.HTTPError as e:
        logger.error(f"Webhook failed ({e.response.status_code if e.response else 'no response'}): {str(e)}")
    except Exception as e:
        logger.error(f"Webhook failed: {str(e)}")
    return False