import json
from pathlib import Path
from datetime import datetime

src = Path("app/logs/social_post_plan.json")
data = json.loads(src.read_text(encoding="utf-8"))

print("=== TODAY FREE TRAFFIC TASKS ===")
print("Date:", datetime.now().strftime("%Y-%m-%d"))
print()

for i, item in enumerate(data["items"], 1):
    print(f"{i}. {item['title']}")
    print("Platforms:", ", ".join(item["platforms"]))
    print("Post:", item["post"])
    print("Hashtags:", " ".join(item["hashtags"]))
    print("CTA:", item["cta"])
    print()
