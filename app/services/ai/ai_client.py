from openai import AsyncOpenAI
from app.config.settings import settings
import logging

logger = logging.getLogger(__name__)

class AIClient:
    def __init__(self):
        self.client = AsyncOpenAI(api_key=settings.OPENAI_API_KEY)
        
    async def call_ai(self, system_prompt: str, user_content: str, temperature: float = 0.3) -> str:
        """
        Generic method to call OpenAI API.
        """
        try:
            response = await self.client.chat.completions.create(
                model=settings.OPENAI_MODEL,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_content}
                ],
                temperature=temperature,
            )
            return response.choices[0].message.content or ""
        except Exception as e:
            logger.error(f"OpenAI API call failed: {e}")
            return ""

# Singleton instance
ai_client = AIClient()
