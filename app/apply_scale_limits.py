import json
from pathlib import Path

PERF=Path("app/logs/product_performance.json")
DEC=Path("app/logs/autopilot_decisions.json")

perf=json.loads(PERF.read_text(encoding="utf-8-sig"))
dec=json.loads(DEC.read_text(encoding="utf-8-sig"))

for item in dec:
    pid=item["product_id"]

    if pid not in perf:
        continue

    published=perf[pid].get("published",0)

    if item["action"]=="scale":

        if published>=16:
            item["action"]="pause"
            item["reason"]="Hard limit reached"

        elif published>=8:
            item["action"]="cooldown"
            item["reason"]="Reduce frequency"

DEC.write_text(
    json.dumps(dec,indent=2),
    encoding="utf-8"
)

print("Cooldown rules applied")
