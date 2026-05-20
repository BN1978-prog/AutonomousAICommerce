import json,os,requests
from pathlib import Path
from datetime import datetime,timezone
from dotenv import load_dotenv

load_dotenv()

token=os.getenv("CJ_ACCESS_TOKEN","").strip()

pid="2056264700793372674"

headers={
    "CJ-Access-Token":token,
    "Content-Type":"application/json"
}

url=f"https://developers.cjdropshipping.com/api2.0/v1/product/query?pid={pid}"

result={
    "created_at":datetime.now(timezone.utc).isoformat(),
    "pid":pid
}

try:
    r=requests.get(url,headers=headers,timeout=30)

    result["status_code"]=r.status_code

    try:
        result["response"]=r.json()
    except:
        result["response_text"]=r.text

except Exception as e:
    result["error"]=str(e)

Path("app/logs/cj_product_detail.json").write_text(
    json.dumps(result,indent=2,ensure_ascii=False),
    encoding="utf-8"
)

print(json.dumps(result,indent=2,ensure_ascii=False))

