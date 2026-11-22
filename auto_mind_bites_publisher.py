# -*- coding: utf-8 -*-
"""
Mind Bites - 100% Automated Instagram & Facebook Post Publisher
Publishes 2 high-converting visual notes daily:
1. Slot 1: 11:30 AM IST (06:00 UTC)
2. Slot 2: 08:30 PM IST (15:00 UTC)
Infinite Loop: Cycles infinitely through the approved pool.
"""

import os
import sys
import glob
import time
import json
import shutil
import requests
from datetime import datetime

from caption_engine import generate_image_aware_caption

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
POOL_FILE = os.path.join(BASE_DIR, "mind_bites_pool.json")
TRACKER_FILE = os.path.join(BASE_DIR, "daily_post_tracker.json")
CREDS_FILE = os.path.join(BASE_DIR, "mind_bites_credentials.json")
IMAGES_DIR = os.path.join(BASE_DIR, "Images")

os.makedirs(IMAGES_DIR, exist_ok=True)

# Load Credentials from Environment or local file
FB_PAGE_ACCESS_TOKEN = os.environ.get("FB_PAGE_ACCESS_TOKEN")
FB_PAGE_ID = os.environ.get("FB_PAGE_ID")
IG_USER_ID = os.environ.get("IG_USER_ID")

if not FB_PAGE_ACCESS_TOKEN and os.path.exists(CREDS_FILE):
    try:
        with open(CREDS_FILE, "r", encoding="utf-8") as f:
            creds = json.load(f)
            FB_PAGE_ACCESS_TOKEN = creds.get("PERMANENT_PAGE_ACCESS_TOKEN")
            FB_PAGE_ID = creds.get("PAGE_ID")
            IG_USER_ID = creds.get("IG_USER_ID")
    except Exception as e:
        print(f"Notice reading credentials: {e}")

print(f"Loaded credentials: FB_PAGE_ID={FB_PAGE_ID}, IG_USER_ID={IG_USER_ID}")


def load_pool() -> list:
    if os.path.exists(POOL_FILE):
        try:
            with open(POOL_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            return []
    return []


def save_pool(pool: list):
    with open(POOL_FILE, "w", encoding="utf-8") as f:
        json.dump(pool, f, indent=2, ensure_ascii=False)


def load_tracker() -> list:
    if os.path.exists(TRACKER_FILE):
        try:
            with open(TRACKER_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            return []
    return []


def save_tracker(tracker: list):
    with open(TRACKER_FILE, "w", encoding="utf-8") as f:
        json.dump(tracker, f, indent=2, ensure_ascii=False)


def get_next_item_to_post(pool: list):
    """
    Finds the item with the minimum times_posted.
    Guarantees infinite circular looping with zero deadlocks.
    """
    if not pool:
        return None, 1

    min_posted = min(item.get("times_posted", 0) for item in pool)
    cycle_number = min_posted + 1

    candidates = [item for item in pool if item.get("times_posted", 0) == min_posted]
    candidates.sort(key=lambda x: x.get("last_posted") or "")
    
    return candidates[0], cycle_number


def post_to_instagram(image_url: str, caption: str) -> str:
    """Posts single photo to Instagram Business Account via Meta Graph API."""
    if not IG_USER_ID or not FB_PAGE_ACCESS_TOKEN:
        print("Notice: Instagram credentials not configured.")
        return ""

    print(f"Step 1: Creating Instagram media container for {IG_USER_ID}...")
    container_url = f"https://graph.facebook.com/v21.0/{IG_USER_ID}/media"
    payload = {
        "image_url": image_url,
        "caption": caption,
        "access_token": FB_PAGE_ACCESS_TOKEN
    }

    try:
        resp = requests.post(container_url, data=payload, timeout=30)
        res_json = resp.json()
        container_id = res_json.get("id")
        if not container_id:
            print(f"Failed to create Instagram container: {res_json}")
            return ""

        print(f"Container created successfully: {container_id}. Waiting for processing...")
        time.sleep(10)

        # Step 2: Publish container
        publish_url = f"https://graph.facebook.com/v21.0/{IG_USER_ID}/media_publish"
        pub_payload = {
            "creation_id": container_id,
            "access_token": FB_PAGE_ACCESS_TOKEN
        }
        pub_resp = requests.post(publish_url, data=pub_payload, timeout=30)
        pub_json = pub_resp.json()
        post_id = pub_json.get("id")
        if post_id:
            print(f"✅ Successfully published to Instagram! Post ID: {post_id}")
            return post_id
        else:
            print(f"Failed to publish Instagram container: {pub_json}")
            return ""
    except Exception as e:
        print(f"Instagram publishing exception: {e}")
        return ""


def post_to_facebook(image_url: str, caption: str) -> str:
    """Posts single photo to Facebook Page Feed via Meta Graph API."""
    if not FB_PAGE_ID or not FB_PAGE_ACCESS_TOKEN:
        print("Notice: Facebook Page credentials not configured.")
        return ""

    print(f"Publishing photo to Facebook Page {FB_PAGE_ID}...")
    url = f"https://graph.facebook.com/v21.0/{FB_PAGE_ID}/photos"
    payload = {
        "url": image_url,
        "caption": caption,
        "access_token": FB_PAGE_ACCESS_TOKEN
    }

    try:
        resp = requests.post(url, data=payload, timeout=30)
        res_json = resp.json()
        post_id = res_json.get("id") or res_json.get("post_id")
        if post_id:
            print(f"✅ Successfully published to Facebook Page! Post ID: {post_id}")
            return post_id
        else:
            print(f"Failed to publish to Facebook: {res_json}")
            return ""
    except Exception as e:
        print(f"Facebook publishing exception: {e}")
        return ""


def run_pipeline():
    pool = load_pool()
    if not pool:
        print("Error: Pool is empty! No images to publish.")
        return False

    item, cycle_number = get_next_item_to_post(pool)
    if not item:
        print("No eligible image found in pool.")
        return False

    image_url = item.get("catbox_url")
    title = item.get("title", "Daily Quick Knowledge Note")
    print(f"\n--- Publishing Mind Bites Note: {title} (Cycle {cycle_number}) ---")
    print(f"Image URL: {image_url}")

    caption = generate_image_aware_caption(item.get("image_name", ""), title)

    # 1. Post to Instagram
    ig_post_id = post_to_instagram(image_url, caption)

    # 2. Post to Facebook
    fb_post_id = post_to_facebook(image_url, caption)

    # Update item and pool if at least one succeeded
    if ig_post_id or fb_post_id:
        now_str = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        item["times_posted"] = item.get("times_posted", 0) + 1
        item["last_posted"] = now_str
        save_pool(pool)

        # Update tracker
        tracker = load_tracker()
        tracker_entry = {
            "timestamp": now_str,
            "title": title,
            "image": item.get("image_name"),
            "cycle_number": cycle_number,
            "instagram_post_id": ig_post_id,
            "facebook_post_id": fb_post_id,
            "caption_preview": caption[:80] + "..."
        }
        tracker.append(tracker_entry)
        save_tracker(tracker)

        print("\n🎉 Mind Bites post successfully recorded and saved to tracker!")
        return True
    else:
        print("\n❌ Failed to publish post to both platforms.")
        return False


if __name__ == "__main__":
    success = run_pipeline()
    if not success:
        sys.exit(1)
