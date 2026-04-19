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
    comments: List[str] = Field(default_factory=list)

# --- Stage 1 Filter Data Models ---
class Stage1Post(BaseModel):
    post_id: str = ""
    title: str
    content: str
    score: int = 0
    url: str = ""
    subreddit: str = ""
    comments: List[str] = Field(default_factory=list)
    is_valuable: bool = False
    keep: bool = False
    reason: str = ""
    category: str = ""
    comment_assessment: str = ""
    involvement_needed: bool = False
    actionable_comments: List[str] = Field(default_factory=list)


class RankedPost(BaseModel):
    title: str
    url: str
    summary: str
