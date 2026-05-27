import json
from pathlib import Path

PERFORMANCE=Path("app/logs/product_performance.json")

p=json.loads(PERFORMANCE.read_text(encoding="utf-8-sig"))

restore={
    "non_slip_silicone_pet_feeding_bowl":{
        "published":6,
        "clicks":63,
        "sales":8,
        "score":143
    },
    "cat_tunnel_pet_toy_cat_s_tunnel_foldable_cat_tunnel_cat_drill_bucket_toy":{
        "published":2,
        "clicks":21,
        "sales":0,
        "score":21
    },
    "pet_brush":{
        "published":0,
        "clicks":9,
        "sales":0,
        "score":9
    },
    "pet_slow_feeder_dog_toy_cute_funny_rubber_dog_ball_toy":{
        "published":0,
        "clicks":6,
        "sales":0,
        "score":6
    }
}

for k,v in restore.items():
    p[k]=v

PERFORMANCE.write_text(
    json.dumps(p,indent=2),
    encoding="utf-8"
)

print("Performance restored")
print(json.dumps(restore,indent=2))
