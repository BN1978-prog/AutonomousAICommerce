import json,re
from pathlib import Path

CATALOG=Path("app/logs/product_catalog.json")
PERFORMANCE=Path("app/logs/product_performance.json")

catalog=json.loads(CATALOG.read_text(encoding="utf-8-sig"))
performance=json.loads(PERFORMANCE.read_text(encoding="utf-8-sig"))

seen=set()
clean=[]

for p in catalog:

    pid=p["id"].lower()

    pid=re.sub(r'_\d+$','',pid)
    pid=re.sub(r'[^a-z0-9_]+','_',pid)
    pid=re.sub(r'_+','_',pid)

    p["id"]=pid

    if pid not in seen:
        seen.add(pid)
        clean.append(p)

new_perf={}

for p in clean:
    pid=p["id"]

    if pid in performance:
        new_perf[pid]=performance[pid]
    else:
        new_perf[pid]={
            "published":0,
            "clicks":0,
            "sales":0,
            "score":0
        }

CATALOG.write_text(
    json.dumps(clean,indent=2),
    encoding="utf-8"
)

PERFORMANCE.write_text(
    json.dumps(new_perf,indent=2),
    encoding="utf-8"
)

print("Catalog cleaned")
print("Products:",len(clean))
