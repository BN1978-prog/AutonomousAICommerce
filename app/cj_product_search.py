import json, os, requests
from pathlib import Path
from datetime import datetime, timezone
from dotenv import load_dotenv

load_dotenv()

OUT=Path("app/logs/cj_product_search.json")

token=os.getenv("CJ_ACCESS_TOKEN","").strip()
keyword=os.getenv("CJ_SEARCH_KEYWORD","Scratcher cat toy").strip()

url="https://developers.cjdropshipping.com/api2.0/v1/product/list"

headers={
    "CJ-Access-Token":token,
    "Content-Type":"application/json"
}

params={
    "pageNum":1,
    "pageSize":10,
    "productName":keyword
}

result={
    "created_at":datetime.now(timezone.utc).isoformat(),
    "keyword":keyword,
    "ok":False,
    "status":"not_run"
}

try:
    r=requests.get(url,headers=headers,params=params,timeout=30)
    result["status_code"]=r.status_code
    try:
        result["response"]=r.json()
    except Exception:
        result["response_text"]=r.text[:2000]

    result["ok"]=r.status_code==200
    result["status"]="searched" if result["ok"] else "api_error"

except Exception as e:
    result["status"]="exception"
    result["error"]=str(e)

OUT.write_text(json.dumps(result,indent=2,ensure_ascii=False),encoding="utf-8")
print(json.dumps(result,indent=2,ensure_ascii=False))
