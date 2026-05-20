import json
from pathlib import Path

REGISTRY=Path("app/logs/imported_skus.json")
OUT=Path("app/logs/performance_board.json")

data=json.loads(REGISTRY.read_text(encoding="utf-8"))

winners=[]
losers=[]

for sku,item in data.items():

    decision=item.get("hunter_decision")
    score=item.get("hunter_score",0)

    row={
        "sku":sku,
        "title":item.get("seo_title") or item.get("title"),
        "score":score
    }

    if decision=="boost":
        winners.append(row)

    elif decision=="reduce":
        losers.append(row)

report={
    "winner_count":len(winners),
    "loser_count":len(losers),
    "winners":sorted(
        winners,
        key=lambda x:x["score"],
        reverse=True
    ),
    "losers":sorted(
        losers,
        key=lambda x:x["score"]
    )
}

OUT.write_text(
    json.dumps(report,indent=2),
    encoding="utf-8"
)

print("WINNERS:",len(winners))
print("LOSERS:",len(losers))
