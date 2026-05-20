import json
from pathlib import Path

IMPORTS = Path("app/logs/imported_skus.json")
PROMO = Path("app/logs/promotion_candidates.json")
OUT = Path("app/logs/seo_action_report.json")

imports = json.loads(IMPORTS.read_text(encoding="utf-8"))
promo = json.loads(PROMO.read_text(encoding="utf-8")) if PROMO.exists() else []

items = []

for p in promo:
    sku = p.get("sku")
    meta = imports.get(sku, {})

    title = meta.get("title") or sku
    description = meta.get("description") or ""
    source = meta.get("source")

    actions = []

    if title == sku or len(title) < 25:
        actions.append("improve_title")

    if len(description) < 80:
        actions.append("improve_description")

    if source == "ai_hunter":
        actions.append("add_ai_hunter_tags")

    items.append({
        "sku": sku,
        "score": p.get("score"),
        "current_title": title,
        "description_length": len(description),
        "recommended_actions": actions
    })

OUT.write_text(
    json.dumps(items, indent=2),
    encoding="utf-8"
)

print("SEO ACTION ITEMS:", len(items))
for item in items:
    print(item["sku"], "=>", ", ".join(item["recommended_actions"]))
