from pathlib import Path

p = Path("app/publish_ebay_from_imports.py")
s = p.read_text(encoding="utf-8")

old = '''for sku, meta in imports.items():
    if not sku.startswith("CJ"):
        continue'''

new = '''for sku, meta in imports.items():
    if not (sku.startswith("CJ") or sku.startswith("PET-BOWL")):
        continue'''

if old not in s:
    print("pattern not found")
else:
    s = s.replace(old, new)
    p.write_text(s, encoding="utf-8")
    print("patched publish_ebay_from_imports.py")
