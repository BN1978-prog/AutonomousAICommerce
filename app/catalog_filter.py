import json
from pathlib import Path

INFILE=Path("app/logs/seo_mass_push_plan.json")
OUTFILE=Path("app/logs/seo_mass_push_plan_filtered.json")

data=json.loads(INFILE.read_text(encoding="utf-8"))

pet_words={
"pet","dog","cat","puppy","kitten",
"leash","bowl","carrier","grooming",
"harness","brush","shampoo","bed",
"collar","blanket","toy","feeder"
}

filtered=[]

for item in data:

    text=(
        (item.get("title") or "")+" "+
        (item.get("description") or "")
    ).lower()

    keep=False

    for word in pet_words:
        if word in text:
            keep=True
            break

    if keep:
        filtered.append(item)

OUTFILE.write_text(
    json.dumps(filtered,indent=2),
    encoding="utf-8"
)

print("ORIGINAL:",len(data))
print("FILTERED:",len(filtered))
print("REMOVED:",len(data)-len(filtered))
