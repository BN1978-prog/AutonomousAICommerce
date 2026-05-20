import json
import re
from pathlib import Path

INFILE = Path("app/logs/traffic_execution_plan_full.json")
OUTFILE = Path("app/logs/traffic_execution_plan_clean.json")

data = json.loads(INFILE.read_text(encoding="utf-8"))

stop_words = {
    "your","with","from","four","large",
    "perfect","style","pets","friend"
}

clean=[]

for item in data:

    desc=item.get("seo_description","")

    # ?????? html
    desc=re.sub(r"<[^>]+>", "", desc)

    # ?????? AI-????????
    if "AI generated Shopify draft product" in desc:
        desc="Premium product selected for quality, comfort and everyday use."

    tags=[]

    for t in item.get("seo_tags",[]):

        t=t.lower().replace(",","").strip()

        if len(t)<4:
            continue

        if t in stop_words:
            continue

        if t not in tags:
            tags.append(t)

    item["seo_description"]=desc[:180]
    item["seo_tags"]=tags[:5]

    clean.append(item)

OUTFILE.write_text(
    json.dumps(clean,indent=2),
    encoding="utf-8"
)

print("CLEANED:",len(clean))
