import json, webbrowser, requests, os, hashlib
from pathlib import Path
from datetime import datetime, timezone

ENV = Path(".env")
for line in ENV.read_text(encoding="utf-8-sig").splitlines():
    if "=" in line and not line.strip().startswith("#"):
        k, v = line.split("=", 1)
        os.environ[k.strip()] = v.strip()

SRC = Path("app/logs/priority_publish_queue.txt")
OUT = Path("app/logs/auto_publish_or_fallback_result.json")
NEXT = Path("app/logs/next_post_to_publish.txt")
POSTED_LOG = Path("app/logs/published_posts.json")

page_id = os.getenv("META_PAGE_ID")
token = os.getenv("META_PAGE_ACCESS_TOKEN")

text = SRC.read_text(encoding="utf-8-sig").replace("\ufeff", "").replace("ï»¿", "")
posts = [p.strip() for p in text.split("--- PRIORITY POST ---") if p.strip()]

if POSTED_LOG.exists():
    published = json.loads(POSTED_LOG.read_text(encoding="utf-8"))
else:
    published = []

published_hashes = {x.get("hash") for x in published}

selected_post = None
selected_hash = None

for post in posts:
    h = hashlib.sha256(post.encode("utf-8")).hexdigest()
    if h not in published_hashes:
        selected_post = post
        selected_hash = h
        break

if not selected_post:
    result = {
        "created_at": datetime.now(timezone.utc).isoformat(),
        "posted": False,
        "reason": "No unpublished posts found"
    }
    OUT.write_text(json.dumps(result, indent=2), encoding="utf-8")
    print(json.dumps(result, indent=2))
    raise SystemExit

NEXT.write_text(selected_post, encoding="utf-8")

result = {
    "created_at": datetime.now(timezone.utc).isoformat(),
    "mode": "try_api_then_fallback",
    "posted": False,
    "fallback_ready": True,
    "hash": selected_hash
}

if page_id and token:
    r = requests.post(
        f"https://graph.facebook.com/v25.0/{page_id}/feed",
        data={
            "message": selected_post,
            "access_token": token
        },
        timeout=30
    )

    try:
        response = r.json()
    except Exception:
        response = {"raw": r.text}

    result["status_code"] = r.status_code
    result["response"] = response
    result["posted"] = r.status_code in [200, 201] and "id" in response

    if result["posted"]:
        published.append({
            "created_at": result["created_at"],
            "post_id": response.get("id"),
            "hash": selected_hash,
            "text_preview": selected_post[:200]
        })
        POSTED_LOG.write_text(json.dumps(published, indent=2), encoding="utf-8")

if not result["posted"]:
    webbrowser.open("https://business.facebook.com/latest/home")
    webbrowser.open("https://www.instagram.com/")
    result["message"] = "Meta API blocked or failed. Post copied to fallback file."

OUT.write_text(json.dumps(result, indent=2), encoding="utf-8")
print(json.dumps(result, indent=2))
