import json
from pathlib import Path
from datetime import datetime, timezone

OUT = Path("app/logs/manual_social_publish_log.json")

record = {
    "created_at": datetime.now(timezone.utc).isoformat(),
    "channels": ["Meta", "Instagram"],
    "posts_published": 3,
    "status": "MANUAL_SOCIAL_POSTS_PUBLISHED"
}

OUT.write_text(json.dumps(record, indent=2), encoding="utf-8")
print(json.dumps(record, indent=2))
