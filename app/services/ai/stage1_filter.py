import json
import logging
import time
from pathlib import Path
from app.models.post_models import RawPost, Stage1Post
from app.services.ai.ai_client import ai_client
from app.utils.validate_ai_output import validate_json_output

logger = logging.getLogger(__name__)

async def filter_posts(posts: list[RawPost]) -> list[Stage1Post]:
    """
    Runs Stage 1 AI filtering on raw posts.
    """
    if not posts:
        return []

    prompt_path = Path(__file__).resolve().parent / "prompts" / "filter_prompt.txt"
    with prompt_path.open("r", encoding="utf-8") as f:
        system_prompt = f.read()
        
    # Build a lookup for metadata by title so AI output can be matched back
    post_meta = {
        p.title: {
            "post_id": p.post_id,
            "url": p.url,
            "subreddit": p.subreddit,
            "score": p.score,
            "comments": p.comments,
        }
        for p in posts
    }

    # Prepare input for AI
    ai_input_data = []
    for post in posts:
        ai_input_data.append({
            "title": post.title,
            "content": post.content,
            "score": post.score,
            "comments": post.comments
        })
        
    user_content = json.dumps(ai_input_data, indent=2)
    logger.info(f"Sending {len(posts)} posts to Stage 1 AI Filter.")
    
    # Retry logic (1 retry)
    max_retries = 2
    for attempt in range(max_retries):
        ai_output = await ai_client.call_ai(system_prompt, user_content)
        parsed_json = validate_json_output(ai_output)
        
        if parsed_json is not None:
            # Parse into Pydantic models
            stage1_posts = []
            for item in parsed_json:
                try:
                    title = item.get("title", "")
                    meta = post_meta.get(title, {})
                    is_valuable = item.get("is_valuable")
                    if is_valuable is None:
                        is_valuable = item.get("keep")
                    if is_valuable is None:
                        # Backward compatibility: if the model only returns kept items,
                        # treat each returned item as valuable.
                        is_valuable = True
                    stage1_post = Stage1Post(
                        post_id=meta.get("post_id", ""),
                        title=title,
                        content=meta.get("content", ""),
                        score=meta.get("score", 0),
                        url=meta.get("url", ""),
                        subreddit=meta.get("subreddit", ""),
                        comments=meta.get("comments", []),
                        is_valuable=is_valuable,
                        keep=is_valuable,
                        reason=item.get("reason", ""),
                        category=item.get("category", ""),
                        comment_assessment=item.get("comment_assessment", ""),
                        involvement_needed=item.get("involvement_needed", False),
                        actionable_comments=item.get("actionable_comments", [])
                    )
                    if stage1_post.is_valuable:
                        stage1_posts.append(stage1_post)
                except Exception as e:
                    logger.error(f"Error parsing AI output item to Stage1Post model: {e}")
            
            logger.info(f"Stage 1 filtering complete. Kept {len(stage1_posts)} posts after comment-based validation.")
            return stage1_posts
            
        logger.warning(f"Stage 1 AI output invalid. Attempt {attempt + 1} of {max_retries}. Retrying...")
    
    logger.error("Stage 1 AI filtering failed after retries.")
    return []
