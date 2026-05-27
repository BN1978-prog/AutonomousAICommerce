from pathlib import Path

p=Path("app/autopilot_runner.py")
text=p.read_text(encoding="utf-8-sig")

# удаляем случайно вставленные кривые строки
bad = [
'run_step("etsy_connection_status", "python -m app.etsy_connection_status")',
'run_step("etsy_autopilot", "python -m app.etsy_autopilot")'
]

lines=text.splitlines()
clean=[]

for line in lines:
    if line.strip() in bad:
        continue
    clean.append(line)

text="\n".join(clean)

# вставляем после crm_readiness_summary с тем же отступом
anchor='    run_step("crm_readiness_summary", "python -m app.crm_readiness_summary")'

replacement='''    run_step("crm_readiness_summary", "python -m app.crm_readiness_summary")
    run_step("etsy_connection_status", "python -m app.etsy_connection_status")
    run_step("etsy_autopilot", "python -m app.etsy_autopilot")'''

text=text.replace(anchor,replacement)

p.write_text(text,encoding="utf-8")

print("autopilot indentation fixed")
