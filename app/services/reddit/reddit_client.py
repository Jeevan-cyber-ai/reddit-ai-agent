import httpx
import asyncio
import logging

logger = logging.getLogger(__name__)

BASE_URL = "https://www.reddit.com"

# Browser User-Agent works better than bot UA for Reddit's public JSON endpoints
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36",
    "Accept": "application/json, text/plain, */*",
    "Accept-Language": "en-US,en;q=0.9",
    "Referer": "https://www.reddit.com/",
}

async def reddit_get(path: str, params: dict = None) -> dict | list:
    """
    Makes a GET request to Reddit's public JSON API.
    Adds a small delay to avoid rate limiting (Reddit allows ~60 req/min).
    `path` example: '/r/FIRE_IND/top.json'
    """
    if params is None:
        params = {}
    params["raw_json"] = 1  # Prevents Reddit from HTML-encoding characters

    url = f"{BASE_URL}{path}"

    async with httpx.AsyncClient(headers=HEADERS, follow_redirects=True) as client:
        # Small delay to be polite and avoid 429/403 rate limits
        await asyncio.sleep(0.1)
        try:
            response = await client.get(url, params=params, timeout=15.0)
            if response.status_code == 403:
                logger.warning(f"403 Blocked for {url} — subreddit may be private or restricted.")
                return {}
            if response.status_code == 429:
                logger.warning(f"429 Rate limited for {url}. Waiting 5s and retrying...")
                await asyncio.sleep(5)
                response = await client.get(url, params=params, timeout=15.0)
            response.raise_for_status()
            return response.json()
        except httpx.HTTPStatusError as e:
            logger.error(f"HTTP error for {url}: {e}")
            return {}
        except Exception as e:
            logger.error(f"Request failed for {url}: {e}")
            return {}
