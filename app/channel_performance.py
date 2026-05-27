import json
from pathlib import Path
from datetime import datetime, timezone

METRICS = Path("app/logs/manual_channel_metrics.json")
OUT = Path("app/logs/channel_performance.json")

metrics = json.loads(
    METRICS.read_text(encoding="utf-8-sig")
)

channels = []

for channel, data in metrics.items():

    if not isinstance(data, dict):
        continue

    clicks = int(data.get("clicks", 0))
    orders = int(data.get("orders", 0))

    score = 50
    score += clicks * 2
    score += orders * 15

    if clicks == 0:
        score -= 5

    channels.append({
        "channel": channel,
        "clicks": clicks,
        "orders": orders,
        "score": max(0, min(score,100))
    })

channels.sort(
    key=lambda x:x["score"],
    reverse=True
)

result = {
    "created_at": datetime.now(timezone.utc).isoformat(),
    "winner": channels[0]["channel"],
    "channels": channels
}

OUT.write_text(
    json.dumps(result, indent=2),
    encoding="utf-8"
)

print(json.dumps(result, indent=2))
