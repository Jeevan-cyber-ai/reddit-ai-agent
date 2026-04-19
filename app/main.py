from fastapi import FastAPI
import httpx
from app.services.reddit.fetch_posts import fetch_top_posts
from app.services.ai.stage1_filter import filter_posts
from app.config.settings import settings

app = FastAPI(title="Reddit AI Digest - Stage 1", description="API to fetch and filter Reddit posts.")

@app.get("/raw-posts")
async def get_parsed_raw_posts():
    """
    Fetches the posts and returns them parsed into our standard RawPost models.
    """
    posts = await fetch_top_posts()
    return {"status": "success", "count": len(posts), "data": posts}

@app.get("/filtered-posts")
async def get_filtered_posts():
    """
    Fetches top posts from all configured subreddits and runs them through
    the Stage 1 AI filter. Returns only meaningful discussions, with Reddit
    URLs and subreddit names included.
    """
    raw_posts = await fetch_top_posts()

    if not raw_posts:
        return {"status": "error", "message": "No posts fetched from Reddit."}

    filtered_posts = await filter_posts(raw_posts)
    return {
        "status": "success",
        "count": len(filtered_posts),
        "data": [post.model_dump() for post in filtered_posts]
    }

@app.get("/reddit-raw-json")
async def get_reddit_raw_json():
    """
    Fetches the EXACT raw JSON from Reddit's API (unparsed) for all configured subreddits.
    """
    all_raw_data = {}
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36",
        "Accept": "application/json"
    }
    
    async with httpx.AsyncClient() as client:
        for subreddit in settings.SUBREDDITS:
            url = f"https://www.reddit.com/r/{subreddit}/top.json?limit={settings.POST_LIMIT}&t=day"
            try:
                response = await client.get(url, headers=headers, follow_redirects=True)
                if response.status_code == 200:
                    all_raw_data[subreddit] = response.json()
                else:
                    all_raw_data[subreddit] = {"error": f"Status code {response.status_code}"}
            except Exception as e:
                all_raw_data[subreddit] = {"error": str(e)}
                
    return {"status": "success", "data": all_raw_data}

@app.post("/run-stage1")
async def run_stage1_filter():
    """
    Fetches the raw posts and runs them through the Stage 1 AI Filter.
    Returns only the meaningful discussions.
    """
    raw_posts = await fetch_top_posts()
    
    if not raw_posts:
        return {"status": "error", "message": "No posts fetched from Reddit."}
        
    filtered_posts = await filter_posts(raw_posts)
    return {"status": "success", "count": len(filtered_posts), "data": filtered_posts}
