def clean_comment_text(text: str) -> str:
    """Removes leading/trailing whitespace and basic markdown noise."""
    if not text:
        return ""
    # Just basic whitespace stripping for now
    return text.strip()

def is_meaningful_comment(text: str) -> bool:
    """Check if comment is long enough to be meaningful (> 20 chars)."""
    return len(text) > 20

def clean_comments(raw_comments: list[str]) -> list[str]:
    """Filters and cleans a list of raw comment strings."""
    cleaned = []
    for comment in raw_comments:
        c_text = clean_comment_text(comment)
        if is_meaningful_comment(c_text) and c_text != "[deleted]" and c_text != "[removed]":
            cleaned.append(c_text)
    return cleaned
