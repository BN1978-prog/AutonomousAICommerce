from pathlib import Path

p = Path("app/seo_report.py")
s = p.read_text(encoding="utf-8")

s = s.replace(
    "normalized = normalize_supplier_product(raw)",
    "try:\n            normalized = normalize_supplier_product(raw)\n        except Exception:\n            continue"
)

p.write_text(s, encoding="utf-8")
print("seo_report patched")
