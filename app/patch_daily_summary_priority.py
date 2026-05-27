from pathlib import Path

p=Path("app/daily_summary.py")
text=p.read_text(encoding="utf-8-sig")

extra=r'''
summary.append("")
summary.append("Next test priorities:")
try:
    pq_path = Path("app/logs/autopilot_priority_queue.json")
    if pq_path.exists():
        pq = json.loads(pq_path.read_text(encoding="utf-8-sig"))
        for item in pq.get("queue", [])[:5]:
            summary.append(
                f"- #{item.get('priority')} {item.get('sku')}: "
                f"score={item.get('exploration_score')}, "
                f"action={item.get('action')}"
            )
    else:
        summary.append("- No priority queue found")
except Exception as e:
    summary.append(f"- Priority queue unavailable: {e}")
'''

needle='Path("app/logs/daily_summary.txt").write_text("\\n".join(summary), encoding="utf-8")'

if "Next test priorities:" not in text:
    text=text.replace(needle, extra + "\n\n" + needle)

p.write_text(text,encoding="utf-8")
print("daily_summary upgraded with priority queue")
