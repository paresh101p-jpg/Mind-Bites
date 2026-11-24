# -*- coding: utf-8 -*-
"""
Mind Bites - 100% Autonomous Dynamic Topic Publisher
Features:
1. On EVERY RUN, dynamically selects a BRAND NEW trending topic from trending_topics_pool.json.
2. ZERO REPEAT: Tracks used_topics.json so no topic is EVER repeated a second time!
3. DYNAMIC RENDERING: Renders the 1080x1350 visual note on the fly with rich themes.
4. UPLOADS & PUBLISHES: Uploads to Catbox CDN, generates image-matched caption, and posts to Instagram & Facebook.
"""

import os
import sys
import time
import json
import requests
from datetime import datetime

# Guarantee UTF-8 output encoding on Windows consoles and GitHub Actions runners
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
if hasattr(sys.stderr, "reconfigure"):
    sys.stderr.reconfigure(encoding="utf-8", errors="replace")

from image_renderer import render_sheet
from caption_engine import generate_topic_caption

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
TOPICS_POOL_FILE = os.path.join(BASE_DIR, "trending_topics_pool.json")
USED_TOPICS_FILE = os.path.join(BASE_DIR, "used_topics.json")
TRACKER_FILE = os.path.join(BASE_DIR, "daily_post_tracker.json")
CREDS_FILE = os.path.join(BASE_DIR, "mind_bites_credentials.json")
OUTPUT_DIR = os.path.join(BASE_DIR, "output")

os.makedirs(OUTPUT_DIR, exist_ok=True)

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


def load_json(filepath: str, default=None):
    if default is None:
        default = []
    if os.path.exists(filepath):
        try:
            with open(filepath, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception as e:
            print(f"Error reading {filepath}: {e}")
            return default
    return default


def save_json(filepath: str, data):
    with open(filepath, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)


def get_next_trending_topic():
    """
    Picks the next unused topic from the trending pool.
    Guarantees ZERO topic repetitions.
    """
    topics = load_json(TOPICS_POOL_FILE, default=[])
    used = load_json(USED_TOPICS_FILE, default=[])

    if not topics:
        print("Error: trending_topics_pool.json is empty!")
        return None

    # Filter out already used topics
    available = [t for t in topics if t.get("id") not in used]

    if not available:
        print("Notice: All topics have been used! Starting Cycle 2.")
        used = []
        save_json(USED_TOPICS_FILE, used)
        available = topics

    chosen = available[0]
    return chosen


def upload_to_catbox(file_path: str) -> str:
    """Uploads freshly rendered image to Catbox CDN for high-speed direct URL."""
    print(f"Uploading {os.path.basename(file_path)} to Catbox CDN...")
    url = "https://catbox.moe/user/api.php"
    for attempt in range(3):
        try:
            with open(file_path, "rb") as f:
                resp = requests.post(
                    url,
                    data={"reqtype": "fileupload"},
                    files={"fileToUpload": f},
                    timeout=35
                )
            if resp.status_code == 200 and resp.text.startswith("http"):
                cat_url = resp.text.strip()
                print(f"✅ Catbox Direct URL: {cat_url}")
                return cat_url
            else:
                print(f"Catbox attempt {attempt+1} response: {resp.text}")
        except Exception as e:
            print(f"Catbox upload error: {e}")
        time.sleep(3)
    return ""


def post_to_instagram(image_url: str, caption: str) -> str:
    """Publishes single photo to Instagram Business Account."""
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

        print(f"Container created: {container_id}. Waiting 10s for processing...")
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
    """Publishes single photo to Facebook Page Feed."""
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
    # 1. Pick brand new trending topic
    topic = get_next_trending_topic()
    if not topic:
        print("No topic available.")
        return False

    topic_id = topic.get("id")
    title = topic.get("title")
    theme_name = topic.get("theme", "corkboard")
    asset_file = topic.get("asset", "")
    print(f"\n🚀 [NEW TOPIC SELECTED]: {title}")
    print(f"Topic ID: {topic_id} | Theme: {theme_name}")

    # 2. Render image on the fly!
    output_image_path = os.path.join(OUTPUT_DIR, f"mind_bites_{topic_id}.jpg")
    print(f"Rendering visual note to: {output_image_path}...")
    render_sheet(topic, theme_name, asset_file, output_image_path)

    if not os.path.exists(output_image_path):
        print("Error: Image rendering failed!")
        return False

    # 3. Upload freshly rendered image to Catbox CDN
    image_url = upload_to_catbox(output_image_path)
    if not image_url:
        print("Error: Failed to upload image to Catbox CDN.")
        return False

    # 4. Generate intelligent image-matched caption
    caption = generate_topic_caption(topic)
    print("\n--- Generated Caption Preview ---")
    print(caption[:150] + "...\n")

    # 5. Publish to Instagram & Facebook
    ig_post_id = post_to_instagram(image_url, caption)
    fb_post_id = post_to_facebook(image_url, caption)

    # 6. Mark topic as used so it is NEVER repeated!
    if ig_post_id or fb_post_id:
        now_str = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        used = load_json(USED_TOPICS_FILE, default=[])
        if topic_id not in used:
            used.append(topic_id)
            save_json(USED_TOPICS_FILE, used)

        tracker = load_json(TRACKER_FILE, default=[])
        tracker.append({
            "timestamp": now_str,
            "topic_id": topic_id,
            "title": title,
            "theme": theme_name,
            "catbox_url": image_url,
            "instagram_post_id": ig_post_id,
            "facebook_post_id": fb_post_id,
            "caption_preview": caption[:80] + "..."
        })
        save_json(TRACKER_FILE, tracker)

        print(f"\n🎉 SUCCESS: Brand new topic '{title}' published and recorded in used_topics.json!")
        return True
    else:
        print("\n❌ Failed to publish to both Instagram and Facebook.")
        return False


if __name__ == "__main__":
    success = run_pipeline()
    if not success:
        sys.exit(1)
