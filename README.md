# Reddit AI Digest - Stage 1 Backend

## Overview
This is a FastAPI-based backend designed to scrape Reddit posts and comments from specific financial subreddits, filter them using an AI-driven pipeline (Stage 1), and expose the high-quality results via a clean API.

The primary goal of this Stage 1 system is to isolate meaningful financial discussions and identify actionable situations where a user is stuck or needs expert involvement.

## What is Completed So Far (Stage 1 Pipeline)
- **Reddit Data Ingestion**: Automatically fetches top daily posts from configured subreddits (`r/indiainvestments`, `r/FIRE_IND`, `r/personalfinanceindia`).
- **Comment Fetching & Cleaning**: Grabs the top 5 direct replies to each post, cleans the text, and filters out noise (e.g., `[deleted]`, `[removed]`, or very short low-effort comments).
- **Stage 1 AI Filtering (OpenAI)**: Evaluates the fetched posts and their comments using `gpt-4o-mini`. It aggressively filters out memes, jokes, and low-effort posts, keeping only meaningful discussions.
- **Actionable Decision Flagging**: The AI explicitly looks for "incomplete decisions" (e.g., someone asking for financial advice, evaluating insurance, or stating they are stuck). It flags these posts with `involvement_needed: true` and extracts the specific questions into an `actionable_comments` array.
- **FastAPI Endpoints**: A set of endpoints to test the raw scraper and the AI pipeline.

## Project Structure
- `app/main.py`: FastAPI application setup and API endpoints.
- `app/config/settings.py`: Application configuration (Target subreddits, API limits, OpenAI config).
- `app/models/post_models.py`: Pydantic models defining the data structure (`RawPost`, `Stage1Post`).
- `app/services/reddit/`: Logic for querying the public Reddit JSON API and parsing the data.
- `app/services/ai/`: Logic for interacting with the OpenAI API and the `filter_prompt.txt`.
- `app/utils/`: Helper functions (e.g., JSON validation, comment cleaning).

## Setup & Running Locally

1. Create and activate a virtual environment:
   ```powershell
   python -m venv venv
   .\venv\Scripts\activate
   ```

2. Install dependencies:
   ```powershell
   pip install -r requirements.txt
   ```

3. Set up your environment variables by creating a `.env` file in the root directory:
   ```env
   OPENAI_API_KEY=your_openai_api_key_here
   ```

4. Start the FastAPI server:
   ```powershell
   uvicorn app.main:app --reload
   ```

5. View the interactive Swagger API documentation at: `http://127.0.0.1:8000/docs`

## API Endpoints
- `GET /raw-posts`: Fetches raw posts and comments from Reddit without applying any AI filtering.
- `POST /run-stage1`: Fetches posts and runs them through the Stage 1 AI Filter, returning *only* the meaningful posts that were kept.
- `GET /reddit-raw-json`: Utility endpoint that fetches the unparsed, raw JSON directly from Reddit.
- `GET /filtered-posts`: Similar to `/run-stage1`, but exposed as a GET request.

## Next Steps for Stage 2 Developer
The Stage 1 pipeline is complete and effectively filtering out the noise. Your job is to pick up where Stage 1 left off.

- You will be consuming the `Stage1Post` JSON output.
- Pay special attention to the `involvement_needed` flag and the `actionable_comments` list in the JSON response. These are highly qualified leads or situations where human intervention is explicitly requested.
- Implement Stage 2 ranking, categorisation, and the final digest generation based on these filtered results.
