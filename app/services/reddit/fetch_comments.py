import logging
from app.config.settings import settings
from app.services.reddit.reddit_client import reddit_get
from app.utils.clean_comments import clean_comments

logger = logging.getLogger(__name__)

async def fetch_comments_for_post(post_id: str, subreddit: str) -> list[str]:
    """
    Fetches the top comments for a given Reddit post using the public JSON API.
    """
    data = await reddit_get(
        f"/r/{subreddit}/comments/{post_id}.json",
        params={"limit": settings.COMMENT_LIMIT, "depth": 1, "sort": "top"}
    )

    # Reddit returns [post_listing, comments_listing]
    if not isinstance(data, list) or len(data) < 2:
        return []

    comments_tree = data[1].get("data", {}).get("children", [])

    raw_comments = []
    for item in comments_tree:
        if item.get("kind") == "t1":  # t1 = comment
            body = item.get("data", {}).get("body", "")
            if body and body not in ("[deleted]", "[removed]"):
                raw_comments.append(body)

    cleaned = clean_comments(raw_comments)
    logger.info(f"Fetched {len(cleaned)} comments for post {post_id}")
    return cleaned[:settings.COMMENT_LIMIT]
