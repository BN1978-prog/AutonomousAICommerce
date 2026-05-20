from pathlib import Path

p=Path("app/daily_run.py")
s=p.read_text(encoding="utf-8")

s=s.replace('    ["python", "-m", "app.profit_report"],\n','')
s=s.replace('    ["python", "-m", "app.seo_report"],\n','')

p.write_text(s,encoding="utf-8")
print("daily_run cleaned: profit_report and seo_report removed")
