import json
from pathlib import Path
from datetime import datetime, timezone

def read_json(path):
    p = Path(path)
    if not p.exists():
        return {}
    try:
        return json.loads(p.read_text(encoding="utf-8-sig"))
    except Exception:
        return {}

health = read_json("app/logs/master_system_health.json")
crm = read_json("app/logs/crm_readiness_summary.json")
meta = read_json("app/logs/meta_launch_readiness.json")
google = read_json("app/logs/google_campaign_live_creator.json")
amazon = read_json("app/logs/amazon_connection_status.json")
priority = read_json("app/logs/autopilot_priority_queue.json")
autopilot = read_json("app/logs/autopilot_run.json")

lines = []
lines.append("AICommerce System Status Report")
lines.append("=" * 40)
lines.append("Created at: " + datetime.now(timezone.utc).isoformat())
lines.append("")

lines.append("Core:")
lines.append("- " + health.get("status", "UNKNOWN"))

lines.append("")
lines.append("CRM:")
lines.append("- " + crm.get("status", "UNKNOWN"))
lines.append("- channel: " + str(crm.get("channel_status")))
lines.append("- smtp: " + str(crm.get("smtp_status")))
lines.append("- send_allowed: " + str(crm.get("send_allowed")))

lines.append("")
lines.append("Meta:")
lines.append("- " + meta.get("status", "UNKNOWN"))
lines.append("- launch_mode: " + str(meta.get("launch_mode")))
lines.append("- live_money_spending: " + str(meta.get("live_money_spending")))

lines.append("")
lines.append("Google:")
lines.append("- " + google.get("status", "UNKNOWN"))
lines.append("- live_money_spending: " + str(google.get("live_money_spending")))

lines.append("")

etsy = read_json("app/logs/etsy_connection_status.json")
etsy_auto = read_json("app/logs/etsy_autopilot.json")

lines.append("")
lines.append("Etsy:")
lines.append("- " + etsy.get("status", "UNKNOWN"))
lines.append("- autopilot: " + etsy_auto.get("status", "UNKNOWN"))

lines.append("Amazon:")
lines.append("- " + amazon.get("status", "UNKNOWN"))
missing = amazon.get("missing", [])
if missing:
    lines.append("- missing: " + ", ".join(missing))

lines.append("")
lines.append("Next test priorities:")
for item in priority.get("queue", [])[:5]:
    lines.append(
        f"- #{item.get('priority')} {item.get('sku')}: "
        f"score={item.get('exploration_score')}, "
        f"action={item.get('action')}"
    )

lines.append("")

actions = read_json("app/logs/action_executor.json")

lines.append("")
lines.append("Action executor:")
lines.append("- " + actions.get("status", "UNKNOWN"))
lines.append("- actions_created: " + str(actions.get("actions_created", 0)))
for item in actions.get("actions", [])[:10]:
    lines.append(
        f"- {item.get('sku')}: {item.get('action')} -> {item.get('status')}"
    )

lines.append("Last autopilot steps:")
for step in autopilot.get("steps", [])[-10:]:
    lines.append(f"- {step.get('name')}: {step.get('status')}")

out = Path("app/logs/system_status_report.txt")
out.write_text("\n".join(lines), encoding="utf-8")

print("\n".join(lines))
