import json
from pathlib import Path
from datetime import datetime, timezone

INP=Path("app/logs/social_content_plan.json")
OUT=Path("app/logs/social_content_enhanced.json")

data=json.loads(
    INP.read_text(encoding="utf-8-sig")
) if INP.exists() else {}

templates={

"pet_brush":{
"hook":"Tired of pet hair everywhere?",
"benefit":"Keep grooming fast and stress-free.",
"cta":"Shop now"
},

"cat_tunnel":{
"hook":"Give indoor cats a new playground.",
"benefit":"Fun movement and stimulation in one foldable tunnel.",
"cta":"Discover more"
},

"slow_feeder":{
"hook":"Turn feeding time into play time.",
"benefit":"Helps reduce boredom and keeps pets engaged.",
"cta":"Shop now"
}

}

posts=[]

for p in data.get("posts",[]):

    sku=p["sku"]

    selected=None

    for k in templates:
        if k in sku.lower():
            selected=templates[k]

    if selected is None:
        selected={
            "hook":"Make pet care easier.",
            "benefit":"Selected products for everyday pet owners.",
            "cta":"Shop now"
        }

    posts.append({
        "sku":sku,
        "platforms":p["platforms"],
        "status":"marketing_ready",
        "post_text":
            f'{selected["hook"]} '
            f'{selected["benefit"]} '
            f'{selected["cta"]}',
        "mode":"draft_only_no_publish"
    })

report={
"created_at":datetime.now(timezone.utc).isoformat(),
"posts_created":len(posts),
"posts":posts,
"status":"SOCIAL_CONTENT_ENHANCED_READY"
}

OUT.write_text(
    json.dumps(report,indent=2),
    encoding="utf-8"
)

print(json.dumps(report,indent=2))
