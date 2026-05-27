from pathlib import Path

p = Path("app/autopilot_runner.py")
text = p.read_text(encoding="utf-8-sig")

lines = text.splitlines()
seen = set()
out = []

for line in lines:
    key = None

    if 'run_step("shopify_crm_events"' in line:
        key = "shopify_crm_events"

    if 'run_step("crm_personalized_drafts"' in line:
        key = "crm_personalized_drafts"

    if key:
        if key in seen:
            continue
        seen.add(key)

    out.append(line)

p.write_text("\n".join(out) + "\n", encoding="utf-8")

print("CRM duplicate steps removed")
