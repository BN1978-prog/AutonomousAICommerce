from pathlib import Path

p=Path("app/auto_disable_skus.py")
s=p.read_text(encoding="utf-8")

s=s.replace('''    if status!="imported":
        reasons.append("not_imported")

''','')

p.write_text(s,encoding="utf-8")
print("not_imported rule removed")
