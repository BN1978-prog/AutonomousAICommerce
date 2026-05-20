import json
from pathlib import Path
from datetime import datetime, timezone

IMPORTS=Path("app/logs/imported_skus.json")
OUT=Path("app/logs/traffic_execution_plan_full.json")

data=json.loads(IMPORTS.read_text(encoding="utf-8"))

plan=[]

for sku,item in data.items():

    title=item.get("title","")

    tags=[]

    words=title.lower().replace("-"," ").split()

    for w in words:
        if len(w)>=4 and w not in tags:
            tags.append(w)

    tags=tags[:5]

    plan.append({
        "sku":sku,
        "seo_title":title,
        "seo_description":(
            item.get("description","")[:180]
        ),
        "seo_tags":tags,
        "auto_apply":True,
        "generated_at":datetime.now(timezone.utc).isoformat()
    })

OUT.write_text(
    json.dumps(plan,indent=2),
    encoding="utf-8"
)

print("SEO PLAN GENERATED:",len(plan))
