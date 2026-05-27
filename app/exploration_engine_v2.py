from app.alert_dispatcher import notify
import json
from pathlib import Path
from datetime import datetime, timezone

SRC = Path("app/logs/product_performance.json")
OUT = Path("app/logs/exploration_v2.json")

data = json.loads(SRC.read_text(encoding="utf-8"))

updated=[]

for sku,p in data.items():

    published=p.get("published",0)
    sales=p.get("sales",0)
    clicks=p.get("clicks",0)
    score=p.get("score",0)

    cooldown=False
    reason=None

    if published>=5 and sales==0:
        cooldown=True
        reason="high_exposure_no_sales"

    boost=0

    if published==0:
        boost+=15
    elif clicks<3:
        boost+=10
    elif clicks<10:
        boost+=5

    winner=(sales>=3)

    if winner:
        boost=max(boost-10,0)

    final_score=score+boost

    updated.append({
        "sku": sku,
        "published": published,
        "sales": sales,
        "clicks": clicks,
        "score": score,
        "winner": winner,
        "cooldown": cooldown,
        "cooldown_reason": reason,
        "exploration_boost": boost,
        "exploration_score": final_score
    })

updated=sorted(
    updated,
    key=lambda x:(
        x["winner"],
        x["cooldown"],
        -x["exploration_score"]
    )
)

report={
    "created_at":datetime.now(timezone.utc).isoformat(),
    "products_processed":len(updated),
    "cooldown_count":len([x for x in updated if x["cooldown"]]),
    "winner_count":len([x for x in updated if x["winner"]]),
    "top_candidates":[x for x in updated if not x["winner"]][:10],
    "top_winners":[x for x in updated if x["winner"]][:5],
    "status":"EXPLORATION_ENGINE_V2_READY"
}

try:
    winners = report.get("top_winners", [])
    if winners:
        top = winners[0]
        sku = top.get("sku", "unknown")
        score = top.get("score", "unknown")
        notify("WINNER_PRODUCT", f"{sku} | score={score}")
        print(f"WINNER ALERT SENT: {sku} score={score}")
except Exception as e:
    print("winner alert skipped:", e)


OUT.write_text(
    json.dumps(report,indent=2),
    encoding="utf-8"
)

print("Products:",len(updated))
print("Winners:",report["winner_count"])
print("Cooldown:",report["cooldown_count"])
