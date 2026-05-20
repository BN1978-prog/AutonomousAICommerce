from pathlib import Path

p=Path("app/main.py")
s=p.read_text(encoding="utf-8")

old='''    for p in products:
        sku = (p.get("sku") or "").strip()'''

new='''    for p in products:
        sku=""

        variants=p.get("variants",[])

        if variants:
            sku=(variants[0].get("sku") or "").strip()'''

s=s.replace(old,new)

p.write_text(
    s,
    encoding="utf-8"
)

print("catalog sku fix applied")
