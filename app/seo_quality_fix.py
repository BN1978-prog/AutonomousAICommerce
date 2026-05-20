import json
from pathlib import Path
from datetime import datetime, timezone

REGISTRY=Path("app/logs/imported_skus.json")
OUT=Path("app/logs/seo_quality_fix_results.json")

fixes={
    "CJJJCWMY01054":{
        "seo_title":"Professional Pet Grooming Scissors for Dogs and Cats",
        "seo_description":"Sharp and comfortable grooming scissors designed for safe pet coat trimming at home."
    },
    "CJMY1174239":{
        "seo_title":"Compact Pet Carrier Bag for Cats and Small Dogs",
        "seo_description":"Lightweight pet carrier designed for comfortable travel with cats and small dogs."
    },
    "CJJJCWMY01010":{
        "seo_title":"Boxed Cat Scratcher Toy for Indoor Cats",
        "seo_description":"Durable boxed cat scratcher designed to keep indoor cats active and entertained."
    },
    "CJJJCWMY00923":{
        "seo_title":"Interactive Cat Scratcher Toy for Daily Play",
        "seo_description":"Fun cat scratcher toy designed for daily play, scratching and indoor activity."
    },
    "CJJJCWGY02924":{
        "seo_title":"Waterproof Dog Raincoat for Outdoor Walks",
        "seo_description":"Lightweight waterproof dog raincoat designed to keep pets dry during rainy walks."
    },
    "CJJJCWGY01083":{
        "seo_title":"Waterproof Dog Socks for Paw Protection",
        "seo_description":"Comfortable waterproof dog socks designed to help protect paws during daily use."
    },
    "CJSP2733732":{
        "seo_title":"Gentle Pet Shampoo for Dogs and Cats",
        "seo_description":"Gentle pet shampoo suitable for keeping dog and cat coats clean, fresh and soft."
    }
}

data=json.loads(REGISTRY.read_text(encoding="utf-8"))

results=[]

for sku,fix in fixes.items():

    if sku not in data:
        results.append({
            "sku":sku,
            "ok":False,
            "reason":"missing_sku"
        })
        continue

    data[sku]["seo_title"]=fix["seo_title"]
    data[sku]["seo_description"]=fix["seo_description"]
    data[sku]["seo_quality_fixed"]=True
    data[sku]["seo_quality_fixed_at"]=datetime.now(timezone.utc).isoformat()

    results.append({
        "sku":sku,
        "ok":True,
        "title":fix["seo_title"]
    })

REGISTRY.write_text(
    json.dumps(data,indent=2),
    encoding="utf-8"
)

OUT.write_text(
    json.dumps(results,indent=2),
    encoding="utf-8"
)

print("FIXED:",sum(1 for x in results if x["ok"]))
