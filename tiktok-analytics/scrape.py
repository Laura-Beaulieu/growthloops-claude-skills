#!/usr/bin/env python3
"""
TikTok Scraper for the tiktok-analytics Claude Code skill.

Pulls public video data from any TikTok handle using Apify's free TikTok scraper.
Normalizes the data and saves it for analysis.

Usage:
    python3 scrape.py @username
    python3 scrape.py username

Requires:
    - APIFY_API_TOKEN in environment or .env file
    - pip install requests python-dotenv
"""

import sys
import os
import json
import time
import argparse
from datetime import datetime, timezone

try:
    import requests
except ImportError:
    print("ERROR: 'requests' package is required. Install it with: pip3 install requests")
    sys.exit(1)

try:
    from dotenv import load_dotenv
except ImportError:
    print("ERROR: 'python-dotenv' package is required. Install it with: pip3 install python-dotenv")
    sys.exit(1)


# Load .env from repo root or current directory
for env_path in [
    os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), ".env"),
    os.path.join(os.getcwd(), ".env"),
]:
    if os.path.exists(env_path):
        load_dotenv(env_path)
        break


APIFY_BASE_URL = "https://api.apify.com/v2"
ACTOR_ID = "clockworks~free-tiktok-scraper"

# View tier thresholds
TIER_VIRAL = 10000
TIER_STRONG = 5000
TIER_AVERAGE = 1000


def get_api_token():
    """Get the Apify API token from environment."""
    token = os.environ.get("APIFY_API_TOKEN")
    if not token:
        print("ERROR: APIFY_API_TOKEN not found.")
        print("Set it in your environment or add it to a .env file:")
        print("  APIFY_API_TOKEN=your_token_here")
        print("")
        print("Get your token at: https://console.apify.com/account/integrations")
        sys.exit(1)
    return token


def clean_handle(handle):
    """Remove @ prefix if present."""
    return handle.lstrip("@").strip()


def assign_tier(views):
    """Assign a performance tier based on view count."""
    if views >= TIER_VIRAL:
        return "viral"
    elif views >= TIER_STRONG:
        return "strong"
    elif views >= TIER_AVERAGE:
        return "average"
    else:
        return "low"


def extract_hashtags(text):
    """Pull hashtags from video description."""
    if not text:
        return []
    return [word.lower() for word in text.split() if word.startswith("#")]


def extract_hook(text):
    """Get the first line of the description as the hook."""
    if not text:
        return ""
    lines = text.strip().split("\n")
    first_line = lines[0].strip()
    # Remove hashtags from hook
    words = first_line.split()
    hook_words = [w for w in words if not w.startswith("#")]
    return " ".join(hook_words).strip()


def parse_datetime(date_value):
    """Parse a date value from the API response. Handles strings and epoch integers."""
    if not date_value:
        return None
    # If it's an integer or numeric string, treat as epoch seconds
    if isinstance(date_value, (int, float)):
        try:
            return datetime.fromtimestamp(int(date_value), tz=timezone.utc)
        except (ValueError, OSError):
            return None
    if isinstance(date_value, str):
        # Check if it's a numeric string (epoch)
        try:
            epoch = int(date_value)
            return datetime.fromtimestamp(epoch, tz=timezone.utc)
        except ValueError:
            pass
        # Try ISO format
        for fmt in [
            "%Y-%m-%dT%H:%M:%S.%fZ",
            "%Y-%m-%dT%H:%M:%SZ",
            "%Y-%m-%dT%H:%M:%S",
            "%Y-%m-%d %H:%M:%S",
            "%Y-%m-%d",
        ]:
            try:
                return datetime.strptime(date_value, fmt).replace(tzinfo=timezone.utc)
            except ValueError:
                continue
    return None


def normalize_video(raw):
    """Normalize a raw video object into a clean schema."""
    # The Apify free TikTok scraper returns various field names.
    # Handle the most common ones.
    video_id = str(
        raw.get("id", "")
        or raw.get("videoId", "")
        or raw.get("aweme_id", "")
    )

    description = (
        raw.get("text", "")
        or raw.get("desc", "")
        or raw.get("description", "")
        or ""
    )

    views = int(
        raw.get("playCount", 0)
        or raw.get("plays", 0)
        or raw.get("views", 0)
        or raw.get("play_count", 0)
        or 0
    )
    likes = int(
        raw.get("diggCount", 0)
        or raw.get("likes", 0)
        or raw.get("digg_count", 0)
        or 0
    )
    comments = int(
        raw.get("commentCount", 0)
        or raw.get("comments", 0)
        or raw.get("comment_count", 0)
        or 0
    )
    shares = int(
        raw.get("shareCount", 0)
        or raw.get("shares", 0)
        or raw.get("share_count", 0)
        or 0
    )
    saves = int(
        raw.get("collectCount", 0)
        or raw.get("saves", 0)
        or raw.get("collect_count", 0)
        or 0
    )

    # Duration
    duration = int(
        raw.get("duration", 0)
        or raw.get("videoLength", 0)
        or raw.get("video_length", 0)
        or 0
    )

    # Date
    date_raw = (
        raw.get("createTime", None)
        or raw.get("created_at", None)
        or raw.get("createTimeISO", None)
        or raw.get("date", None)
    )
    dt = parse_datetime(date_raw)

    date_str = dt.strftime("%Y-%m-%d") if dt else ""
    day_of_week = dt.strftime("%A") if dt else ""
    hour_posted = dt.hour if dt else None

    # Music
    music_info = raw.get("musicMeta", {}) or raw.get("music", {}) or {}
    music = (
        music_info.get("musicName", "")
        or music_info.get("title", "")
        or raw.get("musicTitle", "")
        or ""
    )

    # URL
    author_name = (
        raw.get("authorMeta", {}).get("name", "")
        or raw.get("author", {}).get("uniqueId", "")
        or raw.get("author_name", "")
        or raw.get("authorName", "")
        or ""
    )
    url = raw.get("webVideoUrl", "") or raw.get("url", "") or raw.get("video_url", "")
    if not url and author_name and video_id:
        url = f"https://www.tiktok.com/@{author_name}/video/{video_id}"

    # Engagement rate
    engagement_rate = 0.0
    if views > 0:
        engagement_rate = round(((likes + comments + shares + saves) / views) * 100, 2)

    return {
        "id": video_id,
        "description": description,
        "hook": extract_hook(description),
        "hashtags": extract_hashtags(description),
        "date": date_str,
        "day_of_week": day_of_week,
        "hour_posted": hour_posted,
        "duration_seconds": duration,
        "views": views,
        "likes": likes,
        "comments": comments,
        "shares": shares,
        "saves": saves,
        "engagement_rate": engagement_rate,
        "music": music,
        "url": url,
        "tier": assign_tier(views),
        # These get filled in by Claude during analysis
        "category": "",
        "hook_style": "",
    }


def run_scraper(handle, token):
    """Run the Apify TikTok scraper and return results."""
    url = f"{APIFY_BASE_URL}/acts/{ACTOR_ID}/runs?token={token}"

    payload = {
        "profiles": [handle],
        "resultsPerPage": 100,
        "shouldDownloadCovers": False,
        "shouldDownloadSlideshowImages": False,
        "shouldDownloadSubtitles": False,
        "shouldDownloadVideos": False,
    }

    print(f"Starting Apify scraper for @{handle}...")
    print("This may take 1-3 minutes depending on the account size.")
    print("")

    resp = requests.post(url, json=payload, timeout=30)

    if resp.status_code == 401:
        print("ERROR: Invalid Apify API token. Check your APIFY_API_TOKEN.")
        sys.exit(1)
    elif resp.status_code != 201:
        print(f"ERROR: Apify returned status {resp.status_code}")
        print(resp.text[:500])
        sys.exit(1)

    run_data = resp.json().get("data", {})
    run_id = run_data.get("id")

    if not run_id:
        print("ERROR: No run ID returned from Apify.")
        sys.exit(1)

    print(f"Run started. ID: {run_id}")
    print("Waiting for results", end="", flush=True)

    # Poll for completion
    status_url = f"{APIFY_BASE_URL}/actor-runs/{run_id}?token={token}"
    max_wait = 300  # 5 minutes max
    elapsed = 0
    poll_interval = 5

    while elapsed < max_wait:
        time.sleep(poll_interval)
        elapsed += poll_interval
        print(".", end="", flush=True)

        status_resp = requests.get(status_url, timeout=15)
        if status_resp.status_code != 200:
            continue

        status_data = status_resp.json().get("data", {})
        status = status_data.get("status")

        if status == "SUCCEEDED":
            print(" Done.")
            break
        elif status in ("FAILED", "ABORTED", "TIMED-OUT"):
            print(f"\nERROR: Scraper run {status}.")
            status_msg = status_data.get("statusMessage", "No details available.")
            print(f"Details: {status_msg}")
            sys.exit(1)
    else:
        print("\nERROR: Timed out waiting for scraper results (5 minutes).")
        sys.exit(1)

    # Fetch results
    dataset_id = status_data.get("defaultDatasetId")
    if not dataset_id:
        print("ERROR: No dataset ID found in run results.")
        sys.exit(1)

    results_url = f"{APIFY_BASE_URL}/datasets/{dataset_id}/items?token={token}&format=json"
    results_resp = requests.get(results_url, timeout=30)

    if results_resp.status_code != 200:
        print(f"ERROR: Failed to fetch results. Status: {results_resp.status_code}")
        sys.exit(1)

    items = results_resp.json()
    print(f"Retrieved {len(items)} items from Apify.")
    return items


def main():
    parser = argparse.ArgumentParser(description="Scrape TikTok account data via Apify")
    parser.add_argument("handle", nargs="?", help="TikTok handle (e.g. @username or username)")
    args = parser.parse_args()

    handle = args.handle
    if not handle:
        handle = input("Enter TikTok handle (e.g. @username): ").strip()
    if not handle:
        print("ERROR: No handle provided.")
        sys.exit(1)

    handle = clean_handle(handle)
    token = get_api_token()

    # Run the scraper
    raw_items = run_scraper(handle, token)

    if not raw_items:
        print(f"No videos found for @{handle}. Verify the handle is correct and the account is public.")
        sys.exit(1)

    # Normalize
    videos = []
    for item in raw_items:
        try:
            normalized = normalize_video(item)
            if normalized["id"]:
                videos.append(normalized)
        except Exception as e:
            print(f"Warning: Skipped a video due to error: {e}")

    if not videos:
        print("ERROR: Could not normalize any video data. The API response format may have changed.")
        sys.exit(1)

    # Sort by date descending
    videos.sort(key=lambda v: v["date"], reverse=True)

    # Create output directory
    output_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "output")
    os.makedirs(output_dir, exist_ok=True)

    # Save raw data
    raw_path = os.path.join(output_dir, "raw_data.json")
    with open(raw_path, "w") as f:
        json.dump(raw_items, f, indent=2, default=str)
    print(f"Raw data saved to {raw_path}")

    # Save analyzed data
    analyzed_path = os.path.join(output_dir, "analyzed_data.json")
    analyzed = {
        "handle": handle,
        "scraped_at": datetime.now(timezone.utc).isoformat(),
        "video_count": len(videos),
        "videos": videos,
    }
    with open(analyzed_path, "w") as f:
        json.dump(analyzed, f, indent=2, default=str)
    print(f"Analyzed data saved to {analyzed_path}")

    # Quick summary
    total_views = sum(v["views"] for v in videos)
    avg_views = total_views // len(videos) if videos else 0
    avg_engagement = round(sum(v["engagement_rate"] for v in videos) / len(videos), 2) if videos else 0

    tier_counts = {"viral": 0, "strong": 0, "average": 0, "low": 0}
    for v in videos:
        tier_counts[v["tier"]] += 1

    print("")
    print(f"=== QUICK SUMMARY: @{handle} ===")
    print(f"Videos scraped: {len(videos)}")
    print(f"Total views:    {total_views:,}")
    print(f"Avg views:      {avg_views:,}")
    print(f"Avg engagement: {avg_engagement}%")
    print(f"")
    print(f"Tier breakdown:")
    print(f"  Viral (10K+):    {tier_counts['viral']}")
    print(f"  Strong (5K-10K): {tier_counts['strong']}")
    print(f"  Average (1K-5K): {tier_counts['average']}")
    print(f"  Low (<1K):       {tier_counts['low']}")
    print("")
    print("Next: Claude will categorize videos and generate the full performance report.")


if __name__ == "__main__":
    main()
