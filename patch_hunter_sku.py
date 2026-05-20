from pathlib import Path

p = Path("app/product_hunter/service.py")
s = p.read_text(encoding="utf-8")

old='getattr(opp.source_product,"sku","unknown")'
new='getattr(opp.source_product,"supplier_product_id", getattr(opp.source_product,"sku","unknown"))'

s=s.replace(old,new)

p.write_text(s,encoding="utf-8")

print("hunter sku mapping fixed")
