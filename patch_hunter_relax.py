from pathlib import Path

p=Path("app/product_hunter_runner.py")
s=p.read_text(encoding="utf-8")

s=s.replace('keywords="pet home beauty"', 'keywords="pet"')
s=s.replace('max_unit_cost=15,', 'max_unit_cost=999,')
s=s.replace('min_stock=10,', 'min_stock=0,')
s=s.replace('max_delivery_days=14,', 'max_delivery_days=999,')
s=s.replace('min_opportunity_score=0.70,', 'min_opportunity_score=0.0,')

p.write_text(s,encoding="utf-8")

print("hunter filters relaxed")
