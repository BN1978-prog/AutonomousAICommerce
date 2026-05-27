from pathlib import Path

p=Path("app/system_status_report.py")
text=p.read_text(encoding="utf-8-sig")

extra=r'''
etsy = read_json("app/logs/etsy_connection_status.json")
etsy_auto = read_json("app/logs/etsy_autopilot.json")

lines.append("")
lines.append("Etsy:")
lines.append("- " + etsy.get("status", "UNKNOWN"))
lines.append("- autopilot: " + etsy_auto.get("status", "UNKNOWN"))
'''

anchor='lines.append("Amazon:")'

if "lines.append(\"Etsy:\")" not in text:
    text=text.replace(anchor, extra + "\n" + anchor)

p.write_text(text,encoding="utf-8")
print("Etsy added to system status report")
