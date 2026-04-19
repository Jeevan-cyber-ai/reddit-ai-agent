from pydantic import BaseModel, Field
from typing import List

# --- Raw Reddit Data Models ---
class RawPost(BaseModel):
    post_id: str
    title: str
    content: str
    score: int
    url: str
    subreddit: str = ""
    comments: List[str] = []

# --- Stage 1 Filter Data Models ---
class Stage1Post(BaseModel):
    post_id: str = ""
    title: str
    content: str
    url: str = ""
    subreddit: str = ""
    comments: List[str]
    keep: bool
    reason: str
    involvement_needed: bool = False
    actionable_comments: List[str] = []
