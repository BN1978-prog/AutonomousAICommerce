import json
from pathlib import Path
from datetime import datetime, timezone

IMPORTS = Path("app/logs/imported_skus.json")
PLAN = Path("app/logs/traffic_execution_plan.json")
OUT = Path("app/logs/seo_auto_apply_results.json")

imports = json.loads(IMPORTS.read_text(encoding="utf-8")) if IMPORTS.exists() else {}
plan = json.loads(PLAN.read_text(encoding="utf-8")) if PLAN.exists() else []

results = []

for item in plan:
    sku = item.get("sku")

    for action in item.get("actions", []):
        if action.get("channel") != "seo":
            continue

        if action.get("action") != "apply_seo_suggestion":
            continue

        if action.get("auto_apply") is not True:
            results.append({
                "sku": sku,
                "ok": True,
                "skipped": True,
                "reason": "auto_apply_false"
            })
            continue

        payload = action.get("payload") or {}

        if not payload:
            results.append({
                "sku": sku,
                "ok": False,
                "skipped": True,
                "reason": "missing_seo_payload"
            })
            continue

        if sku not in imports:
            results.append({
                "sku": sku,
                "ok": False,
                "skipped": True,
                "reason": "sku_not_found"
            })
            continue

        imports[sku]["title"] = payload.get("suggested_title")
        imports[sku]["description"] = payload.get("suggested_description")
        imports[sku]["tags"] = payload.get("suggested_tags")
        imports[sku]["seo_auto_applied"] = True
        imports[sku]["seo_auto_applied_at"] = datetime.now(timezone.utc).isoformat()

        results.append({
            "sku": sku,
            "ok": True,
            "skipped": False,
            "reason": "seo_applied_to_registry",
            "title": payload.get("suggested_title")
        })

IMPORTS.write_text(
    json.dumps(imports, indent=2),
    encoding="utf-8"
)

OUT.write_text(
    json.dumps(results, indent=2),
    encoding="utf-8"
)

print("SEO AUTO APPLY RESULTS:", len(results))

for r in results:
    print(
        r["sku"],
        "ok=",
        r["ok"],
        "skipped=",
        r["skipped"],
        "reason=",
        r["reason"]
    )
