import json
import subprocess
import sys
from pathlib import Path
from datetime import datetime, timezone

OUT = Path("app/logs/opportunities/global_arbitrage_report.json")

steps = [
    "app.margin_engine",
    "app.opportunity_engine"
]

results = []

for step in steps:
    p = subprocess.run(
        [sys.executable, "-m", step],
        capture_output=True,
        text=True
    )
    results.append({
        "step": step,
        "ok": p.returncode == 0,
        "returncode": p.returncode,
        "stdout": p.stdout[-3000:],
        "stderr": p.stderr[-3000:]
    })

opp_file = Path("app/logs/opportunities/opportunity_report.json")
opp = json.loads(opp_file.read_text(encoding="utf-8")) if opp_file.exists() else {}

report = {
    "created_at": datetime.now(timezone.utc).isoformat(),
    "mode": "global_arbitrage_safe_analysis",
    "steps_ok": sum(1 for r in results if r["ok"]),
    "steps_total": len(results),
    "opportunities": opp.get("opportunities", 0),
    "top_opportunities": opp.get("top_opportunities", []),
    "execution_allowed": False,
    "reason": "analysis_only_until_platform_rules_and_budget_limits_confirmed",
    "results": results,
    "status": "ok" if all(r["ok"] for r in results) else "error"
}

OUT.write_text(json.dumps(report, indent=2), encoding="utf-8")
print(json.dumps(report, indent=2))
