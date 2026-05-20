import json
from pathlib import Path

REGISTRY=Path("app/logs/imported_skus.json")
OUT=Path("app/logs/dynamic_product_score.json")

data=json.loads(
    REGISTRY.read_text(
        encoding="utf-8"
    )
)

scores=[]

for sku,item in data.items():

    score=0

    hunter=item.get(
        "hunter_score",
        0
    )

    score+=hunter

    if item.get(
        "seo_push_completed"
    ):
        score+=10

    if item.get(
        "seo_quality_fixed"
    ):
        score+=5

    decision=item.get(
        "hunter_decision"
    )

    if decision=="boost":
        score+=15

    elif decision=="reduce":
        score-=20

    elif decision=="exclude":
        score-=100

    scores.append({

        "sku":sku,

        "title":
        item.get("seo_title")
        or item.get("title"),

        "dynamic_score":score
    })

scores=sorted(
    scores,
    key=lambda x:
    x["dynamic_score"],
    reverse=True
)

Path(
"app/logs/dynamic_product_score.json"
).write_text(
    json.dumps(
        scores,
        indent=2
    ),
    encoding="utf-8"
)

print(
    "RANKED:",
    len(scores)
)

print(
    "TOP SCORE:",
    scores[0]["dynamic_score"]
)

print(
    "TOP SKU:",
    scores[0]["sku"]
)
