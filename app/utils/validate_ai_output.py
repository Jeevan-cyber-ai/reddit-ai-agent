import json
import logging
from typing import Any

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def validate_json_output(content: str) -> list[dict[str, Any]] | None:
    """
    Validates that the AI output is valid JSON.
    Strips out markdown code block markers if present.
    """
    content = content.strip()
    if content.startswith("```json"):
        content = content[7:]
    if content.startswith("```"):
        content = content[3:]
    if content.endswith("```"):
        content = content[:-3]
        
    try:
        data = json.loads(content)
        if not isinstance(data, list):
            logger.error("AI output is JSON but not a list.")
            return None
        return data
    except json.JSONDecodeError as e:
        logger.error(f"Failed to parse AI output as JSON: {e}")
        return None


def validate_top_posts_output(content: str) -> list[dict[str, Any]] | None:
    """
    Validates AI output for ranking stages.
    Expected format:
    {
      "top_posts": [
        {"title": "...", "url": "...", "summary": "..."}
      ]
    }
    """
    content = content.strip()
    if content.startswith("```json"):
        content = content[7:]
    if content.startswith("```"):
        content = content[3:]
    if content.endswith("```"):
        content = content[:-3]

    try:
        data = json.loads(content)
    except json.JSONDecodeError as e:
        logger.error(f"Failed to parse ranking output as JSON: {e}")
        return None

    if not isinstance(data, dict):
        logger.error("Ranking output is JSON but not an object.")
        return None

    top_posts = data.get("top_posts")
    if not isinstance(top_posts, list):
        logger.error("Ranking output missing 'top_posts' list.")
        return None

    cleaned: list[dict[str, Any]] = []
    for idx, item in enumerate(top_posts):
        if not isinstance(item, dict):
            logger.error(f"top_posts[{idx}] is not an object.")
            return None
        title = item.get("title")
        url = item.get("url")
        summary = item.get("summary")
        if not isinstance(title, str) or not title.strip():
            logger.error(f"top_posts[{idx}] missing valid title.")
            return None
        if not isinstance(url, str) or not url.strip():
            logger.error(f"top_posts[{idx}] missing valid url.")
            return None
        if not isinstance(summary, str) or not summary.strip():
            logger.error(f"top_posts[{idx}] missing valid summary.")
            return None
        cleaned.append(
            {
                "title": title.strip(),
                "url": url.strip(),
                "summary": summary.strip(),
            }
        )

    return cleaned
