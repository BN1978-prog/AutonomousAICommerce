import json, re
from pathlib import Path

PERFORMANCE = Path("app/logs/product_performance.json")
NEXT = Path("app/logs/next_post_to_publish.txt")

performance = json.loads(PERFORMANCE.read_text(encoding="utf-8-sig"))
text = NEXT.read_text(encoding="utf-8-sig")

m = re.search(r"PRODUCT ID:\s*(.+)", text)
if not m:
    print("No PRODUCT ID found")
    raise SystemExit

product_id = m.group(1).strip()

if product_id not in performance:
    performance[product_id] = {
        "published": 0,
        "clicks": 0,
        "sales": 0,
        "score": 0
    }

performance[product_id]["published"] += 1
performance[product_id]["score"] = (
    performance[product_id]["clicks"] +
    performance[product_id]["sales"] * 10
)

PERFORMANCE.write_text(json.dumps(performance, indent=2), encoding="utf-8")

print("Updated performance for:", product_id)
print(json.dumps(performance[product_id], indent=2))
