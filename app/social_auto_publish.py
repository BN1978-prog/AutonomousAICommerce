import json, os, requests, webbrowser
from pathlib import Path
from datetime import datetime, timezone

ENV = Path(".env")
if ENV.exists():
    for line in ENV.read_text(encoding="utf-8").splitlines():
        if "=" in line and not line.strip().startswith("#"):
            k, v = line.split("=", 1)
            os.environ[k.strip()] = v.strip()

POSTS = Path("app/logs/daily_social_posts_ready.json")
OUT = Path("app/logs/social_auto_publish_results.json")

data = json.loads(POSTS.read_text(encoding="utf-8"))
page_id = os.getenv("META_PAGE_ID")
page_token = os.getenv("META_PAGE_ACCESS_TOKEN")

results = []

for i, post in enumerate(data["posts"], 1):
    text = post["text"]

    if page_id and page_token:
        r = requests.post(
            f"https://graph.facebook.com/v19.0/{page_id}/feed",
            data={
                "message": text,
                "access_token": page_token
            },
            timeout=30
        )

        try:
            response = r.json()
        except Exception:
            response = {"raw": r.text}

        results.append({
            "post": i,
            "channel": "facebook_page",
            "status_code": r.status_code,
            "posted": r.status_code in [200, 201],
            "response": response
        })
    else:
        results.append({
            "post": i,
            "channel": "facebook_page",
            "posted": False,
            "reason": "missing_META_PAGE_ID_or_META_PAGE_ACCESS_TOKEN"
        })

OUT.write_text(json.dumps({
    "created_at": datetime.now(timezone.utc).isoformat(),
    "results": results
}, indent=2), encoding="utf-8")

manual = Path("app/logs/manual_publish_queue.txt")
manual.write_text(
    "\n\n--- POST ---\n\n".join([p["text"] for p in data["posts"]]),
    encoding="utf-8"
)

print(json.dumps({
    "status": "SOCIAL_AUTO_PUBLISH_DONE",
    "results_file": str(OUT),
    "manual_queue": str(manual),
    "results": results
}, indent=2))

webbrowser.open("https://business.facebook.com/latest/home")
webbrowser.open("https://www.pinterest.com/pin-builder/")
webbrowser.open("https://www.tiktok.com/upload")
