from pathlib import Path

p = Path("app/suppliers/normalize_product.py")
s = p.read_text(encoding="utf-8")

old = '"image": image,'
new = '''"image": image,
        "inventory": int(raw.get("inventory") or raw.get("stock") or raw.get("listedNum") or 10),'''

s = s.replace(old, new)

p.write_text(s, encoding="utf-8")
print("inventory fixed")
