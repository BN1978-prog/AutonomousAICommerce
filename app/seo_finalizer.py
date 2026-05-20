import json
import re
from pathlib import Path

INFILE=Path("app/logs/traffic_execution_plan_clean.json")
OUTFILE=Path("app/logs/traffic_execution_plan_final.json")

data=json.loads(INFILE.read_text(encoding="utf-8"))

generic_titles={
    "Pet Brush":"Premium Pet Grooming Brush",
    "Pet travel bag":"Portable Pet Travel Carrier Bag",
    "Dog leash dog leash pet leash":"Durable Dog Leash for Everyday Walks"
}

clean=[]

for item in data:

    title=item["seo_title"]

    if title in generic_titles:
        item["seo_title"]=generic_titles[title]

    desc=item.get("seo_description","")

    # ??????? URL
    desc=re.sub(r'https?://\S+','',desc)

    # ??????? ??????? html/img
    desc=re.sub(r'<[^>]*>','',desc)

    # ??????? ?????
    desc=re.sub(r'img src.*','',desc,flags=re.I)

    desc=desc.replace("Free UK deliver","Free UK delivery")

    desc=' '.join(desc.split())

    if len(desc)<30:
        desc="Premium product selected for quality, comfort and everyday use."

    item["seo_description"]=desc[:180]

    clean.append(item)

OUTFILE.write_text(
    json.dumps(clean,indent=2),
    encoding="utf-8"
)

print("FINAL CLEAN:",len(clean))
