import os
import json
import requests
from datetime import datetime, timezone
from urllib.parse import urljoin
from dotenv import load_dotenv

# ========== CONFIGURATION ==========

load_dotenv()

DISCOURSE_BASE_URL = "https://discourse.onlinedegree.iitm.ac.in/"
CATEGORY_SLUG = "courses/tds-kb"
CATEGORY_ID = 34
START_DATE = "2024-11-01"
END_DATE = "2025-04-15"

RAW_COOKIE_STRING = os.getenv("DISCOURSE_COOKIES", "")
OUTPUT_DIR = "app/data/raw/discourse"
POST_ID_BATCH_SIZE = 50
MAX_CONSECUTIVE_PAGES_WITHOUT_NEW_TOPICS = 5

# ====================================


def parse_cookie_string(raw_cookie_string):
    cookies = {}
    for cookie_part in raw_cookie_string.strip().split(";"):
        if "=" in cookie_part:
            key, value = cookie_part.strip().split("=", 1)
            cookies[key] = value
    return cookies


def get_topic_ids(base_url, category_slug, category_id, start_date_str, end_date_str, cookies):
    url = urljoin(base_url, f"c/{category_slug}/{category_id}.json")
    topic_ids = []
    page = 0

    start_dt = datetime.fromisoformat(
        start_date_str + "T00:00:00").replace(tzinfo=timezone.utc)
    end_dt = datetime.fromisoformat(
        end_date_str + "T23:59:59").replace(tzinfo=timezone.utc)

    last_known_unique_topic_count = 0
    consecutive_stale_pages = 0

    while True:
        paginated_url = f"{url}?page={page}"
        try:
            response = requests.get(paginated_url, cookies=cookies, timeout=30)
            response.raise_for_status()
            data = response.json()
        except Exception as e:
            print(f"❌ Failed to fetch page {page}: {e}")
            break

        topics_on_page = data.get("topic_list", {}).get("topics", [])
        if not topics_on_page:
            print("No more topics found.")
            break

        before_count = len(set(topic_ids))
        for topic in topics_on_page:
            created_at = topic.get("created_at")
            if created_at:
                try:
                    created_dt = datetime.fromisoformat(
                        created_at.replace("Z", "+00:00"))
                    if start_dt <= created_dt <= end_dt:
                        topic_ids.append(topic["id"])
                except Exception:
                    continue

        after_count = len(set(topic_ids))
        if after_count == before_count:
            consecutive_stale_pages += 1
        else:
            consecutive_stale_pages = 0

        if consecutive_stale_pages >= MAX_CONSECUTIVE_PAGES_WITHOUT_NEW_TOPICS:
            break

        if not data.get("topic_list", {}).get("more_topics_url"):
            break

        page += 1

    return list(set(topic_ids))


def get_full_topic_json(base_url, topic_id, cookies):
    initial_url = urljoin(base_url, f"t/{topic_id}.json")
    try:
        response = requests.get(initial_url, cookies=cookies, timeout=30)
        response.raise_for_status()
        topic_data = response.json()
    except Exception as e:
        print(f"❌ Error fetching topic {topic_id}: {e}")
        return None

    stream = topic_data.get("post_stream", {})
    all_ids = stream.get("stream", [])
    existing_posts = {p["id"]: p for p in stream.get("posts", [])}
    missing_ids = [pid for pid in all_ids if pid not in existing_posts]

    if not missing_ids:
        return topic_data

    fetched = []
    for i in range(0, len(missing_ids), POST_ID_BATCH_SIZE):
        batch_ids = missing_ids[i:i + POST_ID_BATCH_SIZE]
        post_url = urljoin(base_url, f"t/{topic_id}/posts.json")
        params = [("post_ids[]", pid) for pid in batch_ids]
        try:
            res = requests.get(post_url, params=params,
                               cookies=cookies, timeout=60)
            res.raise_for_status()
            posts = res.json().get("posts", [])
            fetched.extend(posts)
        except Exception as e:
            print(f"⚠️ Error batch-fetching posts: {e}")

    all_posts = list(existing_posts.values()) + fetched
    post_map = {p["id"]: p for p in all_posts}
    sorted_posts = [post_map[pid] for pid in all_ids if pid in post_map]
    topic_data["post_stream"]["posts"] = sorted_posts
    return topic_data


def save_topic_json(topic_id, topic_data, output_dir):
    os.makedirs(output_dir, exist_ok=True)
    path = os.path.join(output_dir, f"topic_{topic_id}.json")
    with open(path, "w", encoding="utf-8") as f:
        json.dump(topic_data, f, indent=2, ensure_ascii=False)


def main():
    print("📌 Starting Discourse scrape")
    cookies = parse_cookie_string(RAW_COOKIE_STRING)
    topic_ids = get_topic_ids(
        DISCOURSE_BASE_URL, CATEGORY_SLUG, CATEGORY_ID, START_DATE, END_DATE, cookies)

    if not topic_ids:
        print("❌ No topics found in date range.")
        return

    print(
        f"✅ Found {len(topic_ids)} topics between {START_DATE} and {END_DATE}")

    for i, topic_id in enumerate(topic_ids, 1):
        print(f"[{i}/{len(topic_ids)}] ⏳ Fetching topic {topic_id}")
        data = get_full_topic_json(DISCOURSE_BASE_URL, topic_id, cookies)
        if data:
            save_topic_json(topic_id, data, OUTPUT_DIR)
            print(f"✅ Saved topic {topic_id}")
        else:
            print(f"❌ Skipped topic {topic_id}")

    print(f"\n🎉 Done. JSON files saved to: {os.path.abspath(OUTPUT_DIR)}")


if __name__ == "__main__":
    main()
