import json
from pathlib import Path
from datetime import datetime, timezone

PERF = Path("app/logs/channel_performance.json")
QUEUE = Path("app/logs/manual_publish_queue_with_utm.txt")
OUT = Path("app/logs/traffic_priority_plan.json")
TXT = Path("app/logs/priority_publish_queue.txt")

perf = json.loads(PERF.read_text(encoding="utf-8"))
winner = perf["winner"]

raw = QUEUE.read_text(encoding="utf-8")
posts = [p.strip() for p in raw.split("--- POST ---") if p.strip()]

priority_posts = []

for post in posts:
    if f"utm_source={winner}" in post:
        priority = "high"
    else:
        priority = "normal"

    priority_posts.append({
        "priority": priority,
        "winner_channel": winner,
        "post": post
    })

priority_posts.sort(key=lambda x: 0 if x["priority"] == "high" else 1)

result = {
    "created_at": datetime.now(timezone.utc).isoformat(),
    "winner_channel": winner,
    "posts": priority_posts
}

OUT.write_text(json.dumps(result, indent=2), encoding="utf-8")

TXT.write_text(
    "\n\n--- PRIORITY POST ---\n\n".join(
        [
            f"PRIORITY: {p['priority']}\nCHANNEL WINNER: {winner}\n\n{p['post']}"
            for p in priority_posts
        ]
    ),
    encoding="utf-8"
)

print(json.dumps(result, indent=2))
