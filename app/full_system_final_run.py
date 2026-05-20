import subprocess
import sys
import json
from pathlib import Path
from datetime import datetime, timezone

OUT=Path("app/logs/full_system_final_run.json")

steps=[
    "app.channel_validation_checkpoint",
    "app.shopify_write_validation",
    "app.ebay_write_validation",
    "app.ebay_write_offer_validation",
    "app.woocommerce_validation",
    "app.woocommerce_write_validation",
    "app.shopify_registry_hydrator",
    "app.registry_quality_report",
    "app.feed_mass_regenerator",
    "app.feed_channel_validation",
    "app.real_sales_collector",
    "app.sales_cleanup",
    "app.real_sales_mode",
    "app.autopilot_runner",
    "app.autonomous_loop_health",
    "app.final_system_checkpoint"
]

results=[]

print("FULL SYSTEM FINAL RUN START")

for step in steps:
    print("="*60)
    print("RUN:",step)

    p=subprocess.run(
        [sys.executable,"-m",step],
        capture_output=True,
        text=True
    )

    results.append({
        "step":step,
        "ok":p.returncode==0,
        "returncode":p.returncode,
        "stdout":p.stdout[-2500:],
        "stderr":p.stderr[-2500:],
        "finished_at":datetime.now(timezone.utc).isoformat()
    })

    if p.stdout:
        print(p.stdout)

    if p.stderr:
        print("STDERR:")
        print(p.stderr)

    if p.returncode!=0:
        print("STOPPED AT:",step)
        break

ok=sum(1 for x in results if x["ok"])

report={
    "created_at":datetime.now(timezone.utc).isoformat(),
    "ok_steps":ok,
    "total_steps":len(results),
    "all_ok":ok==len(steps),
    "results":results
}

OUT.write_text(json.dumps(report,indent=2),encoding="utf-8")

print("="*60)
print("FULL SYSTEM FINAL RUN COMPLETE")
print("OK:",ok,"/",len(steps))
print("ALL OK:",ok==len(steps))
print("REPORT:",OUT)
