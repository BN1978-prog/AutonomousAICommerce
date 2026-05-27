import json
from pathlib import Path

f = Path("app/logs/pricing_experiments.json")
data = json.loads(f.read_text(encoding="utf-8"))

filtered = [
    x for x in data
    if x["sku"] != "CJJT2896696"
]

f.write_text(json.dumps(filtered, indent=2), encoding="utf-8")

print("REMOVED:", len(data)-len(filtered))
print("REMAINING:", len(filtered))
