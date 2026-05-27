import json
from pathlib import Path

exp = Path("app/logs/exploration_v2.json")
perf = Path("app/logs/product_performance.json")
out = Path("app/logs/autopilot_priority_queue.json")

e = json.loads(exp.read_text(encoding="utf-8"))

queue=[]

for i,p in enumerate(e.get("top_candidates",[])[:10],1):

    queue.append({
        "priority": i,
        "sku": p["sku"],
        "exploration_score": p["exploration_score"],
        "action":"increase_testing"
    })

out.write_text(
    json.dumps({
        "queue_size":len(queue),
        "queue":queue,
        "status":"AUTOPILOT_PRIORITY_QUEUE_READY"
    },indent=2),
    encoding="utf-8"
)

print("Priority queue:",len(queue))
