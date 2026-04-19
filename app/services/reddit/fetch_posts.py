import asyncio
import logging
from app.config.settings import settings
from app.models.post_models import RawPost
from app.services.reddit.reddit_client import reddit_get
from app.services.reddit.fetch_comments import fetch_comments_for_post

logger = logging.getLogger(__name__)

async def _process_post(item: dict, subreddit: str) -> RawPost:
    post_data = item.get("data", {})
    post_id = post_data.get("id", "")
    permalink = post_data.get("permalink", "")

    comments = await fetch_comments_for_post(post_id, subreddit)

    return RawPost(
        post_id=post_id,
        title=post_data.get("title", ""),
        content=post_data.get("selftext", ""),
        score=post_data.get("score", 0),
        url=f"https://www.reddit.com{permalink}",
        subreddit=subreddit,
        comments=comments
    )

async def fetch_top_posts() -> list[RawPost]:
    """
    Fetches top posts from all configured subreddits using Reddit's public JSON API.
    """
    all_posts = []

    for subreddit in settings.SUBREDDITS:
        data = await reddit_get(
            f"/r/{subreddit}/top.json",
            params={"limit": settings.POST_LIMIT, "t": "day"}
        )

        children = data.get("data", {}).get("children", [])
        if not children:
            logger.warning(f"No posts returned for r/{subreddit} (may be private or blocked).")
            continue

        logger.info(f"Fetched {len(children)} posts from r/{subreddit}. Fetching comments...")

        # Concurrently fetch comments for all posts in this subreddit
        tasks = [_process_post(item, subreddit) for item in children]
        subreddit_posts = await asyncio.gather(*tasks)
        all_posts.extend(subreddit_posts)

    return all_posts
