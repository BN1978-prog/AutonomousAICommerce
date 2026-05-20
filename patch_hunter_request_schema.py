from pathlib import Path

p=Path("app/product_hunter_runner.py")
s=p.read_text(encoding="utf-8")

s=s.replace(
'keywords=["pet", "home", "beauty"],',
'keywords="pet home beauty",'
)

s=s.replace(
'min_opportunity_score=70,',
'min_opportunity_score=0.70,'
)

p.write_text(s,encoding="utf-8")
print("hunter request schema fixed")
