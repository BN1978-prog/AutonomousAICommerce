import json
from pathlib import Path

REGISTRY=Path("app/logs/imported_skus.json")
OUT=Path("app/logs/seo_quality_report.json")

data=json.loads(REGISTRY.read_text(encoding="utf-8"))

bad=[]

for sku,item in data.items():

    title=(item.get("seo_title") or "").strip()

    score=100

    words=title.split()

    if len(words)<4:
        score-=30

    if len(title)<25:
        score-=20

    generic_words={
        "pet",
        "large",
        "small",
        "beauty",
        "boxed"
    }

    found=[]

    for w in generic_words:
        if w in title.lower():
            found.append(w)
            score-=10

    if score<70:

        bad.append({
            "sku":sku,
            "score":score,
            "title":title,
            "issues":found
        })

OUT.write_text(
    json.dumps(
        bad,
        indent=2
    ),
    encoding="utf-8"
)

print("LOW QUALITY:",len(bad))

for x in bad:
    print(
        x["sku"],
        x["score"],
        x["title"]
    )
