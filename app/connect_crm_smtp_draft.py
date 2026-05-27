from pathlib import Path

p=Path(".env")
text=p.read_text(encoding="utf-8-sig")

settings={
    "CRM_CHANNEL":"smtp",
    "CRM_ENABLED":"true",
    "CRM_MODE":"draft_only",
    "CRM_REAL_SEND_ENABLED":"false",
    "CRM_MAX_DAILY_SENDS":"0"
}

lines=[]
for line in text.splitlines():
    if "=" in line:
        k=line.split("=",1)[0].strip()
        if k in settings:
            continue
    lines.append(line)

for k,v in settings.items():
    lines.append(f"{k}={v}")

p.write_text("\n".join(lines)+"\n",encoding="utf-8")
print("CRM SMTP draft-only connected")
