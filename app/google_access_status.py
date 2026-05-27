import json
import os
from pathlib import Path
from datetime import datetime, timezone
from dotenv import load_dotenv

load_dotenv(override=True)

OUT = Path("app/logs/google_access_status.json")

developer_token = os.getenv("GOOGLE_ADS_DEVELOPER_TOKEN", "")
refresh_token = os.getenv("GOOGLE_ADS_REFRESH_TOKEN", "")
customer_id = os.getenv("GOOGLE_ADS_CUSTOMER_ID", "")

report = {
    "created_at": datetime.now(timezone.utc).isoformat(),
    "developer_token_present": bool(developer_token),
    "refresh_token_present": bool(refresh_token),
    "customer_id_present": bool(customer_id),
    "status":
        "GOOGLE_CONFIG_PRESENT_WAITING_BASIC_ACCESS"
        if developer_token and refresh_token and customer_id
        else
        "GOOGLE_CONFIG_INCOMPLETE"
}

OUT.write_text(json.dumps(report, indent=2), encoding="utf-8")
print(json.dumps(report, indent=2))
