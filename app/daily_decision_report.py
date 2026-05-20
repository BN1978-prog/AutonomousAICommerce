import json
from pathlib import Path

OUT = Path("app/logs/daily_decision_report.md")

def load_json(path, default):
    p = Path(path)
    return json.loads(p.read_text(encoding="utf-8")) if p.exists() else default

promotion = load_json("app/logs/promotion_actions.json", [])
pricing = load_json("app/logs/pricing_experiments.json", [])
conversion = load_json("app/logs/conversion_watch.json", [])
disable = load_json("app/logs/disable_candidates.json", [])

lines = []
lines.append("# Daily Decision Report")
lines.append("")
lines.append("## Summary")
lines.append(f"- Promotion actions: {len(promotion)}")
lines.append(f"- Pricing experiments: {len(pricing)}")
lines.append(f"- Conversion watch items: {len(conversion)}")
lines.append(f"- Disable candidates: {len(disable)}")
lines.append("")

lines.append("## Promotion Actions")
for item in promotion:
    lines.append(f"- {item.get('sku')}: {', '.join(item.get('actions', []))}")
lines.append("")

lines.append("## Pricing Experiments")
for item in pricing:
    lines.append(
        f"- {item.get('sku')}: {item.get('current_price')} -> {item.get('test_price')} ({item.get('strategy')})"
    )
lines.append("")

lines.append("## Conversion Watch")
for item in conversion[:20]:
    lines.append(
        f"- {item.get('sku')}: days={item.get('days_live')}, sales={item.get('sales')}, action={item.get('recommended_action')}"
    )

OUT.write_text("\n".join(lines), encoding="utf-8")

print("DAILY DECISION REPORT:", OUT)
print(OUT.read_text(encoding="utf-8"))
