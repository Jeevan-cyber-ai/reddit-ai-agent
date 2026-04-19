from pydantic_settings import BaseSettings
from typing import List

class Settings(BaseSettings):
    # Reddit config
    SUBREDDITS: List[str] = [
        "indiainvestments",
        "FIRE_IND",
        "personalfinanceindia"
    ]
    POST_LIMIT: int = 10
    COMMENT_LIMIT: int = 5

    # OpenAI config
    OPENAI_API_KEY: str = ""
    OPENAI_MODEL: str = "gpt-4o-mini"

    # Email config
    EMAIL_USER: str = ""
    EMAIL_PASS: str = ""
    EMAIL_RECEIVER: str = ""

    model_config = {
        "env_file": ".env",
        "extra": "ignore"
    }


settings = Settings()
