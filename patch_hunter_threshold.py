from pathlib import Path

p=Path("app/product_hunter/service.py")
s=p.read_text(encoding="utf-8")

s=s.replace(
'opp.opportunity_score >= 80',
'opp.opportunity_score >= 0.80'
)

p.write_text(s,encoding="utf-8")
print("promotion threshold fixed")
