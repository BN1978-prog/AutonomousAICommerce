import subprocess
import sys
from datetime import datetime, timezone
import json
from pathlib import Path

OUT = Path("app/logs/pipeline_runner_results.json")

steps = [
    "app.shopify_registry_hydrator",
    "app.registry_quality_report",
    "app.seo_auto_apply",
    "app.seo_push_to_channels",
    "app.seo_push_executor",
    "app.feed_regenerator",
    "app.feed_quality_check",
]

results = []

print("PIPELINE RUNNER START")

for step in steps:
    print("=" * 60)
    print("RUN:", step)

    started_at = datetime.now(timezone.utc).isoformat()

    proc = subprocess.run(
        [sys.executable, "-m", step],
        capture_output=True,
        text=True
    )

    result = {
        "step": step,
        "ok": proc.returncode == 0,
        "returncode": proc.returncode,
        "started_at": started_at,
        "finished_at": datetime.now(timezone.utc).isoformat(),
        "stdout": proc.stdout[-3000:],
        "stderr": proc.stderr[-3000:]
    }

    results.append(result)

    print(proc.stdout)

    if proc.stderr:
        print("STDERR:")
        print(proc.stderr)

    if proc.returncode != 0:
        print("PIPELINE STOPPED AT:", step)
        break

OUT.write_text(json.dumps(results, indent=2), encoding="utf-8")

ok_count = sum(1 for r in results if r["ok"])

print("=" * 60)
print("PIPELINE COMPLETE")
print("STEPS OK:", ok_count, "/", len(results))
print("REPORT:", OUT)
