from pathlib import Path

p=Path("app/product_hunter_runner.py")
s=p.read_text(encoding="utf-8")

s=s.replace(
"    registry = SupplierRegistry(settings)",
"    registry = SupplierRegistry()"
)

p.write_text(s,encoding="utf-8")
print("hunter runner registry fixed")
