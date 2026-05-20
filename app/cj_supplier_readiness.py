import json, os
from pathlib import Path
from datetime import datetime, timezone
from dotenv import load_dotenv

load_dotenv()

OUT=Path("app/logs/cj_supplier_readiness.json")

token=os.getenv("CJ_ACCESS_TOKEN","").strip()
platform_token=os.getenv("CJ_PLATFORM_TOKEN","").strip()

status={
  "created_at":datetime.now(timezone.utc).isoformat(),
  "supplier":"cjdropshipping",
  "ok":bool(token),
  "status":"ready" if token else "missing_env",
  "required_env":["CJ_ACCESS_TOKEN"],
  "optional_env":["CJ_PLATFORM_TOKEN"],
  "present":[k for k,v in {
    "CJ_ACCESS_TOKEN":token,
    "CJ_PLATFORM_TOKEN":platform_token
  }.items() if v],
  "mode":"safe_create_only_no_payment",
  "payType":3
}

OUT.write_text(json.dumps(status,indent=2),encoding="utf-8")
print(json.dumps(status,indent=2))
