import json
from pathlib import Path

DISC=Path("app/logs/meta_assets_discovery.json")
ENV=Path(".env")

data=json.loads(DISC.read_text(encoding="utf-8"))

businesses=data.get("businesses",{}).get("data",{}).get("data",[])

if not businesses:
    raise SystemExit("No Meta business found")

business_id=businesses[0]["id"]

lines=ENV.read_text(encoding="utf-8").splitlines()

lines=[
    x for x in lines
    if not x.startswith("META_BUSINESS_ID=")
]

lines.append(f"META_BUSINESS_ID={business_id}")

ENV.write_text(
    "\n".join(lines)+"\n",
    encoding="utf-8"
)

print("META_BUSINESS_ID=",business_id)
