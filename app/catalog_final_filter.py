import json
from pathlib import Path

INFILE=Path("app/logs/seo_mass_push_plan_filtered.json")
OUTFILE=Path("app/logs/seo_mass_push_plan_final.json")

data=json.loads(INFILE.read_text(encoding="utf-8"))

pet_keywords={
"pet","dog","cat","puppy","kitten",
"leash","bowl","carrier","grooming",
"harness","brush","shampoo","bed",
"collar","blanket","toy","feeder",
"water","raincoat","tunnel","comb"
}

blocked={
"glass",
"microneedle",
"tea",
"flowers",
"cup",
"regeneration"
}

final=[]

for item in data:

    text=(
        (item.get("title","")+" ")+
        (" ".join(item.get("tags",[])))
    ).lower()

    # ????????? ????? ??????
    if any(x in text for x in blocked):
        continue

    # ???????? ?????? pet
    if not any(x in text for x in pet_keywords):
        continue

    final.append(item)

OUTFILE.write_text(
    json.dumps(final,indent=2),
    encoding="utf-8"
)

print("FINAL:",len(final))
