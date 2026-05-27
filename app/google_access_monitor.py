import json
import subprocess
import sys
from pathlib import Path
from datetime import datetime, timezone

OUT = Path("app/logs/google_access_monitor.json")

proc = subprocess.run(
    [sys.executable,"-m","app.token_manager"],
    capture_output=True,
    text=True
)

report = {
    "created_at": datetime.now(timezone.utc).isoformat(),
    "google_ready": False,
    "status": None
}

try:
    data = json.loads(proc.stdout)

    for item in data.get("results",[]):

        if item.get("provider")=="google_ads":

            if item.get("ok"):

                report["google_ready"]=True
                report["status"]="google_api_ready"

            else:

                report["status"]=item.get("status")

except Exception as e:

    report["status"]="parse_error"
    report["error"]=str(e)

OUT.write_text(
    json.dumps(report,indent=2),
    encoding="utf-8"
)

print(
json.dumps(
report,
indent=2
)
)
