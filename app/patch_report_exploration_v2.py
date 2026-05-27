from pathlib import Path

p = Path("app/autopilot_report.py")
text = p.read_text(encoding="utf-8-sig")

extra = r'''
print()
print("Exploration v2:")
try:
    exp_path = Path("app/logs/exploration_v2.json")
    if exp_path.exists():
        exp = json.loads(exp_path.read_text(encoding="utf-8-sig"))
        print("Status:", exp.get("status"))
        print("Cooldown count:", exp.get("cooldown_count"))
        print("Top exploration candidates:")
        for item in exp.get("top_candidates", [])[:5]:
            print(
                "- "
                + str(item.get("id") or item.get("product_id") or item.get("sku") or item.get("title"))
                + ": exploration_score="
                + str(item.get("exploration_score"))
                + ", boost="
                + str(item.get("exploration_boost"))
                + ", cooldown="
                + str(item.get("cooldown"))
            )
    else:
        print("No exploration_v2.json found")
except Exception as e:
    print("Exploration v2 report error:", e)
'''

if "Exploration v2:" not in text:
    text = text + "\n" + extra

p.write_text(text, encoding="utf-8")
print("autopilot_report upgraded with Exploration v2")
