from pathlib import Path

p=Path("app/importer/service.py")
s=p.read_text(encoding="utf-8")

old='''if sku_data["status"]=="imported":
    return sku_data'''

new='''if sku_data["status"] in ["imported","hunter_imported"]:
    return sku_data'''

if old in s:
    s=s.replace(old,new)
    p.write_text(s,encoding="utf-8")
    print("patched importer")
else:
    print("pattern not found")
