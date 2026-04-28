from pathlib import Path
from pydantic_settings import BaseSettings, SettingsConfigDict
from typing import List

class Settings(BaseSettings):
    # Reddit config
    SUBREDDITS: List[str] = [
        "MutualfundsIndia",
        "personalfinanceindia",
        "IndiaInvestments",
        "FIREIndia",
        "fatFIREIndia"
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

    model_config = SettingsConfigDict(
        env_file=Path(__file__).resolve().parent.parent.parent / ".env",
        extra="ignore"
    )


settings = Settings()
