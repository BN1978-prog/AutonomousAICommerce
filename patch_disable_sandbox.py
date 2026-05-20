from pathlib import Path

p=Path("app/suppliers/sandbox_supplier.py")
s=p.read_text(encoding="utf-8")

if "DISABLED_IN_PRODUCTION=True" not in s:
    s="DISABLED_IN_PRODUCTION=True\n"+s

s=s.replace(
'            "sku": "TEST-SUPPLIER-002",',
'            "sku": "DISABLED-TEST-SUPPLIER-002",'
)

p.write_text(s,encoding="utf-8")

print("SANDBOX SUPPLIER DISABLED")
