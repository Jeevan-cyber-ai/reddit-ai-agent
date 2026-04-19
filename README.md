# Reddit AI Digest

FastAPI backend that fetches top Reddit finance discussions, filters low-value posts with OpenAI, ranks the best posts per subreddit, performs a final global ranking, prints the result to console, and emails the final top 3.

## What This Project Does

The pipeline currently works in these stages:

1. Fetch top daily Reddit posts from the configured subreddits.
2. Fetch and clean a small number of top comments for each post.
3. Stage 1: use OpenAI to filter out noisy, low-value, or irrelevant discussions.
4. Stage 2: rank the validated posts separately for each subreddit and keep the top 3.
5. Stage 3: merge the subreddit winners and select the final top 3 overall.
6. Print the final output in the console.
7. Send the same final output by email.

## Project Structure

- `app/main.py` - FastAPI app and pipeline endpoints.
- `app/config/settings.py` - Application settings loaded from `.env`.
- `app/models/post_models.py` - Pydantic models for raw, filtered, and ranked posts.
- `app/services/reddit/` - Reddit API fetching and comment cleanup.
- `app/services/ai/` - OpenAI client, prompts, Stage 1 filter, Stage 2 ranking, Stage 3 ranking.
- `app/services/notifications/email_sender.py` - Gmail SMTP email sender.
- `app/utils/output_formatter.py` - Shared console/email formatting.
- `app/utils/validate_ai_output.py` - JSON validation helpers for AI responses.

## Requirements

- Python 3.11 or newer recommended.
- A Reddit-friendly internet connection.
- OpenAI API key.
- Gmail account with 2-Step Verification enabled and an App Password created.

## Setup

### 1. Clone the repository

```powershell
git clone https://github.com/Jeevan-cyber-ai/reddit-ai-agent.git
cd reddit-ai-agent
```

### 2. Create a virtual environment

Windows:

```powershell
python -m venv venv
```

macOS/Linux:

```bash
python3 -m venv venv
```

### 3. Activate the virtual environment

Windows PowerShell:

```powershell
.\venv\Scripts\activate
```

macOS/Linux:

```bash
source venv/bin/activate
```

### 4. Install dependencies

```powershell
pip install -r requirements.txt
```

### 5. Create the `.env` file

Create a `.env` file in the project root and add:

```env
OPENAI_API_KEY=your_openai_api_key
OPENAI_MODEL=gpt-4o-mini

EMAIL_USER=your_gmail_address@gmail.com
EMAIL_PASS=your_gmail_app_password
EMAIL_RECEIVER=recipient_email@gmail.com
```

Notes:

- `EMAIL_USER` and `EMAIL_RECEIVER` can be the same address if you want to send the digest to yourself.
- Use a Gmail App Password, not your normal Gmail password.

## Run the App

Start the API:

```powershell
uvicorn app.main:app --reload
```

Open Swagger UI:

```text
http://127.0.0.1:8000/docs
```

## Current Configuration

The current settings file uses these subreddits:

- `indiainvestments`
- `FIRE_IND`
- `personalfinanceindia`

If you want to change them, edit `app/config/settings.py`.

## API Endpoints

### GET `/raw-posts`
Returns the raw normalized Reddit posts.

### GET `/filtered-posts`
Runs Stage 1 filtering and returns only valuable posts.

### GET `/reddit-raw-json`
Returns the raw Reddit JSON payload for each configured subreddit.

### POST `/run-stage1`
Runs Stage 1 filtering only.

### POST `/run-ranking-pipeline`
Runs the full pipeline:

1. Fetch raw posts
2. Stage 1 validation/filtering
3. Per-subreddit ranking
4. Global ranking
5. Console output
6. Email delivery

This endpoint returns diagnostic fields as well:

- `stage1_count`
- `stage1_by_subreddit`
- `subreddit_rankings`
- `ranking_error_by_subreddit`
- `merged_count`
- `final_count`
- `final_top_posts`
- `final_output_text`
- `email_status`
- `email_error`

## Output Format

The final console and email content are generated from one shared formatter and look like this:

```text
Top 3 Reddit Finance Insights
================================
Generated At: 2026-04-20 12:34 UTC

Top 3 Posts:
------------

1.
Title: ...
URL: ...
Summary: ...
------------

2.
Title: ...
URL: ...
Summary: ...
------------

3.
Title: ...
URL: ...
Summary: ...
------------
```

## How To Verify It Is Working

### 1. Check that the app starts

```powershell
uvicorn app.main:app --reload
```

You should see Uvicorn running at `http://127.0.0.1:8000`.

### 2. Verify raw posts

Use Swagger or run:

```powershell
Invoke-RestMethod -Method Get -Uri "http://127.0.0.1:8000/raw-posts"
```

### 3. Verify Stage 1 filtering

Use Swagger or run:

```powershell
Invoke-RestMethod -Method Get -Uri "http://127.0.0.1:8000/filtered-posts"
```

### 4. Verify full ranking and email flow

Use Swagger or run:

```powershell
Invoke-RestMethod -Method Post -Uri "http://127.0.0.1:8000/run-ranking-pipeline" | ConvertTo-Json -Depth 8
```

Check the response for:

- `status = success`
- `final_count = 3` or fewer if there are not enough valid posts
- `final_top_posts` with `title`, `url`, `summary`
- `final_output_text` containing the formatted digest
- `email_status = sent`

If email fails, check `email_error`.

## Debugging Notes

### Stage 1 empty for a subreddit

Check:

- `stage1_by_subreddit`
- `ranking_error_by_subreddit`

Possible causes:

- Reddit returned no posts for that subreddit.
- Stage 1 filtered all posts out as low-value.
- AI response was invalid or empty.

### Email failure

If you see a Gmail error like `Application-specific password required`, you need:

1. 2-Step Verification enabled on the Gmail account.
2. A Gmail App Password generated in Google Account settings.
3. That App Password saved in `EMAIL_PASS` inside `.env`.

## Notes for Contributors

- The shared formatter in `app/utils/output_formatter.py` is used by both console printing and email body generation.
- Keep AI responses strict JSON.
- Keep endpoint responses backward-compatible unless you intentionally change the pipeline contract.

## License

No license has been declared yet.
