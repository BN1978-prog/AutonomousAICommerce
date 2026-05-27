from pathlib import Path

p=Path("app/system_status_report.py")
text=p.read_text(encoding="utf-8-sig")

extra=r'''
actions = read_json("app/logs/action_executor.json")

lines.append("")
lines.append("Action executor:")
lines.append("- " + actions.get("status", "UNKNOWN"))
lines.append("- actions_created: " + str(actions.get("actions_created", 0)))
for item in actions.get("actions", [])[:10]:
    lines.append(
        f"- {item.get('sku')}: {item.get('action')} → {item.get('status')}"
    )
'''

anchor='lines.append("Last autopilot steps:")'

if "Action executor:" not in text:
    text=text.replace(anchor, extra + "\n" + anchor)

p.write_text(text,encoding="utf-8")
print("system_status_report upgraded with action executor")
