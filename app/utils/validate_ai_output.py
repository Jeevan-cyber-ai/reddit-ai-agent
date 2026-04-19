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
