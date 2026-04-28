import sys, os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import asyncio
from app.services.ai.stage1_filter import filter_posts
from app.models.post_models import RawPost

async def main():
    sample = RawPost(
        post_id="test",
        title="Test title",
        content="This is a test post content about finance.",
        score=123,
        url="https://reddit.com/r/test/test",
        subreddit="testsub",
        comments=["Nice post!", "I agree."]
    )
    result = await filter_posts([sample])
    print("Result:", result)

if __name__ == "__main__":
    asyncio.run(main())
