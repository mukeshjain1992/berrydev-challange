import httpx
import logging
from app.constant import API_KEY

from tenacity import retry, wait_exponential, stop_after_attempt

logger = logging.getLogger(__name__)


# Define retry strategy
@retry(wait=wait_exponential(multiplier=1, min=4, max=10), stop=stop_after_attempt(3))
async def fetch_with_retries(url: str, headers: dict):
    async with httpx.AsyncClient() as client:
        response = await client.get(url, headers=headers)
        response.raise_for_status()
        return response.json()


async def fetch_crm_data(offset: int = 0, limit: int = 100):
    """
    Fetches CRM data from the Berry API.

    Args:
        offset: The offset to start fetching data from.
        limit: The maximum number of records to fetch.

    Returns:
        A JSON response containing the CRM data.
    """
    headers = {"X-API-Key": API_KEY}
    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(
                f"https://challenge.berrydev.ai/api/crm/customers?offset={offset}&limit={limit}",
                headers=headers,
            )
            response.raise_for_status()
            logger.info(f"Fetched CRM data from Berry API (offset: {offset}, limit: {limit})")
            return response.json()
        except httpx.HTTPError as e:
            fetch_with_retries(f"https://challenge.berrydev.ai/api/crm/customers?offset={offset}&limit={limit}", headers)
            logger.error(f"Failed to fetch CRM data from Berry API: {e}")
            raise e


async def fetch_marketing_data():
    """
    Fetches marketing data from the Berry API.

    Returns:
        A JSON response containing the marketing data.
    """
    headers = {"X-API-Key": API_KEY}
    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(
                "https://challenge.berrydev.ai/api/marketing/campaigns",
                headers=headers,
            )
            response.raise_for_status()
            logger.info("Fetched marketing data from Berry API")
            return response.json()
        except httpx.HTTPError as e:
            fetch_with_retries("https://challenge.berrydev.ai/api/marketing/campaigns", headers)
            logger.error(f"Failed to fetch marketing data from Berry API: {e}")
            raise e

